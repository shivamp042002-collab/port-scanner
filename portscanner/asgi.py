import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portscanner.settings')

# ✅ THIS LINE FIXES YOUR ERROR
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import scanner.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            scanner.routing.websocket_urlpatterns
        )
    ),
})