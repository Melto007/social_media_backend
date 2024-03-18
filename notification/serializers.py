from rest_framework import serializers
from core.models import Follower

class NotficationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['id', 'user', 'following', 'status']
