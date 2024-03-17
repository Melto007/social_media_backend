from rest_framework import (
    status,
    viewsets,
    mixins,
    exceptions
)
from rest_framework.response import Response
from config import authentication
from .serializers import (
    ProfileSerializer,
    FollowingSerializer
)
from core.models import (
    Profile,
    Follower
)
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

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

class FollowingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowingSerializer
    authentication_classes = [authentication.JWTAuthentication]
    queryset = Follower.objects.all()

    def list(self, request):
        try:
            follower = self.queryset.filter(user=request.user)
            serializer = self.get_serializer(follower, many=True)

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
            follower = data.get('follower', None)

            profile = get_user_model().objects.get(name=follower)

            serializer = self.get_serializer(data={'status': True})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, following=profile)

            follower = self.queryset.filter(user=request.user)
            serializer = self.get_serializer(follower, many=True)

            response = {
                'message': 'followers created successfully',
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

    def destroy(self, request, pk):
        try:
            follower = self.queryset.filter(user=request.user, following=pk).first()

            if not follower:
                raise exceptions.APIException('Followers not found')

            follower.delete()

            response = {
                'data': 'follower deleted successfully',
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)