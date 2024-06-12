from rest_framework import serializers
from accounts import serializers as account_serializers
from . import models

class SessionSerializer(serializers.ModelSerializer):

    students = account_serializers.StudentSerializer(many=True, read_only=True)

    admin = account_serializers.AdminSerializer(required=False)

    class Meta:
        model = models.Session
        fields = '__all__'

    def create(self, validated_data):
        validated_data['admin'] = self.context['admin']
        return super().create(validated_data)