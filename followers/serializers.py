from django.contrib.auth import get_user_model
from rest_framework import serializers

""" followers serializer"""
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email']