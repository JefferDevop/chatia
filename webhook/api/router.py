# app_whatsapp/urls.py
from django.urls import path, include
from .views import WhatsAppWebhookAPIView, test_enviar_template

urlpatterns = [
    path('webhook/', WhatsAppWebhookAPIView.as_view(), name='whatsapp_webhook'),
    path('test/send-template/', test_enviar_template, name='test_send_template'),
]