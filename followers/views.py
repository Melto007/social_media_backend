from rest_framework import (
    status,
    viewsets,
    mixins
)
from rest_framework.response import Response
from config import authentication
from .serializers import (
    FollowerSerializer
)
from django.contrib.auth import get_user_model
from django.db.models import Q

""" followers views class """
class FollowersViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowerSerializer
    authentication_classes = [authentication.JWTAuthentication]
    queryset = get_user_model().objects.all()

    """ get all the users """
    def list(self, request):
        try:
            queryset = self.queryset.exclude(Q(email=request.user) | Q(email="admin@gmail.com"))
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