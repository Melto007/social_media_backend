from rest_framework import (
    mixins,
    viewsets,
    status
)
from rest_framework.response import Response
from .serializers import (
    PostSerializer,
    TagSerializer
)
from config.authentication import JWTAuthentication
from core.models import (
    Post,
    Profile,
    Tag
)
from config.cloudinary import upload_image

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

            tag = data.get('tag', None)
            post = data.get('post', None)

            instance = Profile.objects.get(user=request.user)
            tag_exists = Tag.objects.filter(tags=tag)

            if not tag_exists.exists() and tag is not None:
                serializer = TagSerializer(data={'tags': tag})
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = self.get_serializer(data={'post': post})
                serializer.is_valid(raise_exception=True)
                serializer.save(profile=instance)

                response = {
                    'data': 'post created successfully',
                    'status': status.HTTP_200_OK
                }
                return Response(response)

            get_tags = Tag.objects.get(tags=tag)

            serializer = self.get_serializer(data={'post': post})
            serializer.is_valid(raise_exception=True)
            serializer.save(tag=get_tags, profile=instance)

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