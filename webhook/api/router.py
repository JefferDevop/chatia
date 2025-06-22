# app_whatsapp/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import WhatsAppWebhookAPIView, test_enviar_template, WhatsAppAgentViewSet, WhatsAppClientViewSet, WhatsAppConversationViewSet, WhatsAppConversationAgentViewSet, WhatsAppMessageViewSet



# API Router
router = routers.DefaultRouter()
router.register(r'clients', WhatsAppClientViewSet)
router.register(r'agents', WhatsAppAgentViewSet)
router.register(r'conversations', WhatsAppConversationViewSet)
router.register(r'conversation-agents', WhatsAppConversationAgentViewSet)
router.register(r'messages', WhatsAppMessageViewSet)

urlpatterns = [
    path('webhook/', WhatsAppWebhookAPIView.as_view(), name='whatsapp-webhook'),
    path('', include(router.urls)),
    path('test/send-template/', test_enviar_template, name='test_send_template'),
]



