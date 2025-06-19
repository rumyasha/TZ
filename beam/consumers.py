import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Notification
from django.utils import timezone


class NotificationConsumer(AsyncWebsocketConsumer):
    """Улучшенный consumer для уведомлений с полным соответствием ТЗ"""

    # Группы для рассылки
    groups = ["broadcast"]  # Глобальная группа по умолчанию

    async def connect(self):
        """Обработка подключения с аутентификацией"""
        self.user = self.scope["user"]

        # Закрываем соединение для анонимных пользователей
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        # Персональная группа пользователя
        self.user_group = f'user_{self.user.id}'
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        # Группа админов (если пользователь админ)
        if self.user.is_staff:
            await self.channel_layer.group_add(
                "admins",
                self.channel_name
            )

        await self.accept()

        # Отправляем подтверждение подключения
        await self.send_connection_success()

        # Отправляем историю непрочитанных уведомлений
        await self.send_unread_notifications()

    async def disconnect(self, close_code):
        """Обработка отключения с очисткой групп"""
        if hasattr(self, 'user_group'):
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )
        if hasattr(self, 'user') and self.user.is_staff:
            await self.channel_layer.group_discard(
                "admins",
                self.channel_name
            )

    async def receive(self, text_data):
        """Обработка входящих сообщений с валидацией"""
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()

            if not message:
                raise ValueError("Сообщение не может быть пустым")

            # Создаем и сохраняем уведомление
            notification = await self.create_notification(
                message=message,
                extra_data=data.get('data', {})
            )

            # Рассылаем уведомление
            await self.channel_layer.group_send(
                self.user_group,
                {
                    'type': 'send.notification',
                    'notification': await self.serialize_notification(notification)
                }
            )

        except Exception as e:
            await self.send_error_message(str(e))

    async def send_notification(self, event):
        """Отправка уведомления клиенту"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['notification']
        }))

    async def send_connection_success(self):
        """Отправка подтверждения подключения"""
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'status': 'success',
            'user_id': self.user.id,
            'timestamp': timezone.now().isoformat(),
            'message': 'WebSocket соединение установлено'
        }))

    async def send_error_message(self, error_msg):
        """Отправка сообщения об ошибке"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'timestamp': timezone.now().isoformat(),
            'message': error_msg
        }))

    @database_sync_to_async
    def create_notification(self, message, extra_data=None):
        """Создание и сохранение уведомления в БД"""
        return Notification.objects.create(
            user=self.user,
            message=message,
            extra_data=extra_data or {},
            is_read=False
        )

    @database_sync_to_async
    def send_unread_notifications(self):
        """Отправка непрочитанных уведомлений при подключении"""
        notifications = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).order_by('-created_at')[:10]  # Лимит последних 10

        # Отправляем количество
        self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': notifications.count()
        }))

        # Отправляем сами уведомления
        for notification in notifications:
            self.send(text_data=json.dumps({
                'type': 'notification',
                'data': {
                    'id': notification.id,
                    'message': notification.message,
                    'created_at': notification.created_at.isoformat(),
                    'is_read': notification.is_read,
                    'extra_data': notification.extra_data
                }
            }))

    @database_sync_to_async
    def serialize_notification(self, notification):
        """Сериализация уведомления для отправки"""
        return {
            'id': notification.id,
            'message': notification.message,
            'created_at': notification.created_at.isoformat(),
            'is_read': notification.is_read,
            'extra_data': notification.extra_data
        }
