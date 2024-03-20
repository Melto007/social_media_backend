from rest_framework import serializers
from core.models import (
    Post,
    Tag
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tags', 'status']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'profile', 'post', 'tag', 'status']
        depth = 1