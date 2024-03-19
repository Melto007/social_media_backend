from rest_framework import (
    mixins,
    viewsets,
    status
)
from rest_framework.response import Response
from .serializers import PostSerializer
from config.authentication import JWTAuthentication
from core.models import (
    Post,
    Profile
)

class PostViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request):
        try:
            data = request.data
            instance = Profile.objects.get(user=request.user)

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile=instance)

            response = {
                'data': 'post created successfully',
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)