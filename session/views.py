from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import serializers, models
from django.http import HttpRequest
from SmfAttendance.shortcuts import check_permission
from django.shortcuts import get_object_or_404
from accounts import models as account_models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
import json

class SessionView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        
        can_add_session = check_permission('add_session', request)
        admin = get_object_or_404(account_models.Admin, id=request.user.pk)

        if not can_add_session:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = serializers.SessionSerializer(data=request.data, context={'admin' : admin})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk):
        
        can_change_session = check_permission('change_session', request)

        if not can_change_session:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        instance = get_object_or_404(models.Session, id=pk)

        if not(instance.admin.pk == request.user.pk):
            return Response({'detail' : 'You can only update your sessions'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.SessionSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk):
        can_delete_session = check_permission('delete_session', request)

        if not can_delete_session:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        instance = get_object_or_404(models.Session, id=pk)

        if not(instance.admin.pk == request.user.pk):
            return Response({'detail' : 'You can only delete your sessions'}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()
        return Response({'detail' : 'Session deleted Successfully'}, status=status.HTTP_200_OK)

class SessionStudentsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, session_pk: int, student_uuid: str):

        can_change_session = check_permission('change_session', request)

        # check if that is already admin or not add student into session
        if not can_change_session:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        # get session or 404
        session = get_object_or_404(models.Session, id=session_pk)

        # check if that admin is the owner of session or not
        if not(session.admin.pk == request.user.pk):
            return Response({'detail' : 'You can only update your sessions'}, status=status.HTTP_403_FORBIDDEN)
        
        # get student or 404 
        student = get_object_or_404(account_models.Student, uid=student_uuid)

        # finally add student into session
        session.students.add(student)
        
        serializer = serializers.SessionSerializer(instance=session)

        # send the data to websocket connection for real time
        channel_layer: RedisChannelLayer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            session.name, # group name
            {
                "type" : "session_update",
                "data" : json.dumps(serializer.data)
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, session_pk: int, student_uuid: str):

        can_delete_session = check_permission('delete_session', request)

        if not can_delete_session:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        session = get_object_or_404(models.Session, id=session_pk)

        if not(session.admin.pk == request.user.pk):
            return Response({'detail' : 'You can only update your sessions'}, status=status.HTTP_403_FORBIDDEN)
        
        student = get_object_or_404(account_models.Student, uid=student_uuid)

        session.students.remove(student)
        
        serializer = serializers.SessionSerializer(instance=session)

        channel_layer: RedisChannelLayer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            session.name, # group name
            {
                "type" : "session_update",
                "data" : json.dumps(serializer.data)
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

