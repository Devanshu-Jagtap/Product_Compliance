"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.communication.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": django.core.asgi.get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
