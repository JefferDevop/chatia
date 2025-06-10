# app_whatsapp/urls.py



from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import WhatsAppWebhookViewSet


router_webhook = DefaultRouter()
router_webhook.register('webhooks', WhatsAppWebhookViewSet)

