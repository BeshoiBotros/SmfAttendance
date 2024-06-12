from django.urls import path
from .consumers import SessionConsumer

session_socket_routes = [
    path('ws/session/<int:pk>/', SessionConsumer.as_asgi())
]