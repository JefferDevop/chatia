from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, AgentViewSet, TagViewSet,
    ConversationViewSet, MessageViewSet, TaskViewSet,
    WebhookEventViewSet
)

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('agents', AgentViewSet)
router.register('tags', TagViewSet)
router.register('conversations', ConversationViewSet)
router.register('messages', MessageViewSet)
router.register('tasks', TaskViewSet)
router.register('webhooks', WebhookEventViewSet)


