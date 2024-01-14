from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (
    TokenUser
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = { 'password': { 'write_only': True } }

    def create(self, validated_data):
        username = validated_data.pop('name', None)

        if username is None:
            raise serializers.ValidationError("Username is required")

        name = username.replace(" ", "")

        if get_user_model().objects.filter(name=name).exists():
            raise serializers.ValidationError("Username is already exists")

        return get_user_model().objects.create_user(name=name, **validated_data)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUser
        fields = ['id', 'user', 'token']