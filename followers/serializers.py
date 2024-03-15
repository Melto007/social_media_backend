from core.models import (
    Profile,
)
from rest_framework import serializers

""" followers serializer"""
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'url', 'slug']
        depth = 1
        lookup_field = 'slug'