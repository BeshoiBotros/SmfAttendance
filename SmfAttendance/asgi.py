import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from SmfAttendance.shortcuts import get_all_route_list
from session.routing import session_socket_routes
from .JWTAuthMiddleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmfAttendance.settings')


application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : JWTAuthMiddleware(
        URLRouter(
            session_socket_routes
        )
    )
})