from rest_framework import serializers
from core.models import (
    Follower,
    Profile
)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'image', 'url', 'slug', 'status']

class NotficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'user', 'following', 'status', 'userProfile']
        depth = 1
