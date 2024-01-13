from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.response import Response


class UserRegisterMixin(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    def list(self, request):
        return Response("Hello World success")