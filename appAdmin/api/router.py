from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, AgentViewSet, ConversationViewSet, MensajeWhatsAppViewSet

router = DefaultRouter()
router.register(r'clientes', ClientViewSet)
router.register(r'agentes', AgentViewSet)
router.register(r'conversaciones', ConversationViewSet)
router.register(r'mensajes', MensajeWhatsAppViewSet)