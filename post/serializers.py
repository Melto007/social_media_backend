from rest_framework import serializers
from core.models import (
    Post,
    Tag,
    PostImage
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tags', 'status']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'url', 'status']

class PostSerializer(serializers.ModelSerializer):

    postImage = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'post', 'tag', 'status', 'postImage']
        depth = 2