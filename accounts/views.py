from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from SmfAttendance.shortcuts import check_permission

class StudentView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, pk=None):
        
        if pk:
            instance = get_object_or_404(models.Student, id=pk)
            serializer = serializers.StudentSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        queryset = models.Student.objects.all()
        serializer = serializers.StudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        
        can_add_student = check_permission('add_student', request)

        if not can_add_student:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk):
        
        can_change_student = check_permission('change_student', request)

        if not can_change_student:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        instance = get_object_or_404(models.Student, id=pk)

        serializer = serializers.StudentSerializer(instance=instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request: HttpRequest, pk):
        
        can_delete_student = check_permission('delete_student', request)

        if not can_delete_student:
            return Response({'detail' : 'You can not perform this action'}, status=status.HTTP_403_FORBIDDEN)

        instance = get_object_or_404(models.Student, id=pk)

        instance.delete()

        return Response({'detail' : 'student deleted successfully.'}, status=status.HTTP_200_OK)
