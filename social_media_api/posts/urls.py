from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed_view
from django.urls import path

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = router.urls + [
    path('feed/', feed_view, name='feed'),
]