# core/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import app_whatsapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Solo se llama una vez aquí
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app_whatsapp.routing.websocket_urlpatterns
        )
    ),
})


