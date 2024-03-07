from core.models import Profile
from rest_framework import serializers

""" followers serializer"""
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'url']
        depth = 1