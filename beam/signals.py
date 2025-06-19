from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product, Post, Comment, Notification


@receiver(post_save, sender=Product)
def handle_product_notifications(sender, instance, created, **kwargs):
    """Уведомления для продуктов"""
    if created:
        # Уведомление администраторам
        async_to_sync(get_channel_layer().group_send)(
            "admins",
            {
                "type": "send.notification",
                "message": f"Новый продукт: {instance.name}",
                "data": {"type": "product", "id": instance.id}
            }
        )

        # Уведомление создателю
        if instance.created_by:
            Notification.objects.create(
                user=instance.created_by,
                message=f"Вы создали продукт: {instance.name}",
                extra_data={"product_id": instance.id}
            )


@receiver(post_save, sender=Post)
def handle_post_notifications(sender, instance, created, **kwargs):
    """Уведомления для постов"""
    action = "создан" if created else "обновлён"
    async_to_sync(get_channel_layer().group_send)(
        "global_feed",
        {
            "type": "send.notification",
            "message": f"Пост {action}: {instance.title}",
            "data": {
                "type": "post",
                "id": instance.id,
                "action": action
            }
        }
    )


@receiver(post_save, sender=Comment)
def handle_comment_created(sender, instance, created, **kwargs):
    """Уведомления о новых комментариях"""
    if created:
        # Автору поста
        Notification.objects.create(
            user=instance.post.author,
            message=f"Новый комментарий к посту '{instance.post.title}'",
            extra_data={
                "type": "comment",
                "comment_id": instance.id,
                "post_id": instance.post.id
            }
        )


@receiver(post_delete, sender=Comment)
def handle_comment_deleted(sender, instance, **kwargs):
    """Уведомления об удалении комментариев"""
    async_to_sync(get_channel_layer().group_send)(
        f"post_{instance.post.id}_followers",
        {
            "type": "send.notification",
            "message": f"Комментарий удалён из поста '{instance.post.title}'",
            "data": {
                "type": "comment_deleted",
                "post_id": instance.post.id
            }
        }
    )
