from rest_framework import (
    mixins,
    viewsets,
    status
)
from rest_framework.response import Response

class PostViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def create(self, request):
        try:
            response = {
                'data': 'success',
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)