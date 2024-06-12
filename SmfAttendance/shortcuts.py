from django.http import HttpRequest
from session.models import Session
from accounts.models import Admin
from django.shortcuts import get_object_or_404

def get_all_route_list(routing_list: list):
    
    route_of_array = []

    for i in routing_list:
        route_of_array.append(i)

    return route_of_array

def check_permission(permission_name: str, request: HttpRequest):
    for group in request.user.groups.all():
        if group.permissions.filter(codename = permission_name):
            return True
    return False

def sessionOwner(session_pk: int, user_pk: int):
    session = get_object_or_404(Session, id=session_pk)
    admin = get_object_or_404(Admin, id=user_pk)
    if not(session.admin.pk == admin.pk):
        return False
    return True