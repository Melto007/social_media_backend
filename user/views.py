from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework.response import Response
from user.serializer import (
    UserSerializer
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from config import authentication
from .serializer import (
    TokenSerializer
)


""" Register user for class """
class UserRegisterMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        """ Register user """
        try:
            data = request.data

            email = data.get('email', None)
            username = data.get('name', None)
            password = data.get('password', None)
            confirm_password = data.get('confirm_password', None)

            if email is None or not email:
                raise exceptions.APIException("Email is required")

            if username is None or not username:
                raise exceptions.APIException("Username is required")

            if password is None or not password:
                raise exceptions.APIException("password is required")

            if email[-4:0] != 'com' and email[-9:-4] != 'gmail':
                raise exceptions.APIException('Invalid Email')

            if password != confirm_password:
                raise exceptions.APIException("Password and Confirm Password do not match")

            serailizer = self.get_serializer(data=data)
            serailizer.is_valid(raise_exception=True)
            serailizer.save()

            response = {
                'message': 'user registered successfully'
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


""" Login user class """
class LoginMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        try:
            data = request.data

            email = data.get('email', None)
            password = data.get('password', None)

            if email is None or not email:
                raise exceptions.APIException("Email field is required")

            if password is None or not password:
                raise exceptions.APIException("Password field is required")

            user = get_object_or_404(self.queryset, email=email)

            if not user.check_password(password):
                raise exceptions.AuthenticationFailed("Invalid Credential")

            access_token = authentication.create_access_token(user.id)
            refresh_token = authentication.create_refresh_token(user.id)

            response = Response()

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True
            )

            response.data = {
                'token': access_token,
            }

            return response

        except Exception as e:
            response = {
                "message": e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RefreshMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TokenSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            id = authentication.decode_refresh_token(refresh_token)
            access_token = authentication.create_access_token(id)

            response = {
                'token': access_token
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'error': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class HomeMixinView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.JWTAuthentication]

    def list(self, request):
        try:
            serializer = self.get_serializer(request.user)
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)