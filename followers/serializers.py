from core.models import (
    Profile,
    Follower
)
from rest_framework import serializers

""" followers serializer"""
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'url', 'slug']
        depth = 1
        lookup_field = 'slug'

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'user', 'following', 'status', 'userProfile']
        depth = 1

    def create(self, validated_data):
        return Follower.objects.create(**validated_data)