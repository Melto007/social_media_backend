from rest_framework import (
    viewsets,
    mixins,
    status
)
from rest_framework.response import Response
from config.authentication import JWTAuthentication
from core.models import (
    Follower
)
from .serializers import (
    NotficationSerializer
)

class NotificationViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = NotficationSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Follower.objects.all()

    def list(self, request):
        try:
            queryset = self.queryset.filter(user=request.user)
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
            return Response("success")