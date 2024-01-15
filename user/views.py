from rest_framework import (
    viewsets,
    mixins,
    exceptions,
    status
)
from rest_framework import generics
from rest_framework.response import Response
from user.serializer import (
    UserSerializer
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from config import authentication
from config.mail import send_email
from .serializer import (
    TokenSerializer,
    ResetSerializer
)
from core.models import (
    TokenUser,
    Reset
)
import datetime
import random
import string
from django.db.models import Q
from rest_framework.decorators import action


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

            TokenUser.objects.create(user=user.id, token=refresh_token)

            request.session['refresh_token'] = refresh_token

            response = {
                'token': access_token,
            }

            return Response(response, status=status.HTTP_200_OK)

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
    queryset = TokenUser.objects.all()

    def create(self, request):
        try:
            refresh_token = request.session.get('refresh_token', False)

            id = authentication.decode_refresh_token(refresh_token)

            if not self.queryset.filter(
                user=id,
                token=refresh_token,
                expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
            ).exists():
                self.queryset.filter(
                    user=id,
                    token=refresh_token
                ).delete()
                raise exceptions.AuthenticationFailed('Unauthorized User')

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


class LogoutMixin(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TokenSerializer
    queryset = TokenUser.objects.all()
    authentication_classes = [authentication.JWTAuthentication]

    def list(self, request):
        try:
            refresh_token = request.session.get('refresh_token', False)

            if not refresh_token:
                raise exceptions.AuthenticationFailed('Unauthorized User')

            self.queryset.filter(
                user=request.user.id,
                token=refresh_token
            ).delete()

            del request.session['refresh_token']

            response = {
                'message': 'Successfully logout'
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ResetSerializer
    queryset = Reset.objects.all()

    def create(self, request):
        try:
            email = request.data.get('email', None)

            if not get_user_model().objects.filter(email=email).exists():
                raise exceptions.APIException('Invalid Credential')

            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            serializer = self.get_serializer(data={'email': email, 'token': token})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            url = 'Enter this code to reset your password ' + token

            mail = send_email(url, email)

            if mail != 1:
                self.queryset.filter(Q(email=email) & Q(token=token)).delete()
                raise exceptions.APIException("Mail not send")

            response = {
                'message': 'Reset Token generated successfully'
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ResetSerializer
    queryset = Reset.objects.all()

    def create(self, request):
        data = request.data

        code = data.get('code', None)
        password = data.get('password', None)
        confirmpassword = data.get('confirmpassword', None)

        if password != confirmpassword:
            raise exceptions.APIException('password do not match')

        reset_password = self.queryset.filter(token=code).first()

        if not reset_password:
            raise exceptions.APIException('Invalid code')

        user = get_user_model().objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('user not found')

        self.queryset.filter(Q(token=code) & Q(email=reset_password.email)).delete()
        user.set_password(password)
        user.save()

        response = {
            'message': 'Password change successfully'
        }

        return Response(response, status=status.HTTP_200_OK)


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
