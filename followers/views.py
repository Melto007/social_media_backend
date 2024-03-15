from rest_framework import (
    status,
    viewsets,
    mixins
)
from rest_framework.response import Response
from config import authentication
from .serializers import (
    ProfileSerializer,
)
from core.models import (
    Profile,
)
from django.db.models import Q
from django.contrib.auth import get_user_model

""" followers views class """
class FollowersViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProfileSerializer
    authentication_classes = [authentication.JWTAuthentication]
    queryset = Profile.objects.all()
    lookup_field = 'slug'

    """ get all the users """
    def list(self, request):
        try:
            queryset = self.queryset.exclude(Q(user=request.user) | Q(slug='admin'))
            serializer = self.get_serializer(queryset, many=True)
            response = {
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)

    def create(self, request):
        try:
            data = request.data
            sender = data.get('sender', None)
            queryset = Profile.objects.get(slug=sender)
            serializer = self.get_serializer(queryset)

            response = {
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)
