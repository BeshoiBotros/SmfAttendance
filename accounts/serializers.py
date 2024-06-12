from rest_framework import serializers
from . import models

class AdminSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.Admin
        fields = '__all__'



class StudentSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = models.Student
        fields = '__all__'

