# app_whatsapp/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/whatsapp/", consumers.WhatsAppConsumer.as_asgi()),
]
