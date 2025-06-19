from django.contrib import admin
from .models import Product, UserProfile, UserProduct, Notification, Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # убраны 'created_at'
    search_fields = ('name',)
    list_filter = ()  # убран 'created_at'

@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')  # убраны 'purchased_at' и 'quantity'
    raw_id_fields = ('user', 'product')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read')  # убран 'created_at'
    list_filter = ('is_read',)
    search_fields = ('user__username', 'message')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('post', 'author')
    search_fields = ('text', 'author__username')
    raw_id_fields = ('post', 'author')
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
