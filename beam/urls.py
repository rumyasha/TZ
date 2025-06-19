from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

custom_urlpatterns = [
    path('posts/<int:post_id>/comments/',
         views.PostCommentsView.as_view(),
         name='post-comments'),
    path('posts/<int:post_id>/products/',
         views.PostProductsView.as_view(),
         name='post-products'),
    path('users/<int:user_id>/notifications/',
         views.UserNotificationsView.as_view(),
         name='user-notifications'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(custom_urlpatterns)),
    path('ws/notifications/', views.NotificationWebsocketView.as_view(), name='ws-notifications'),
]