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
from config.mail import send_email
from .serializer import (
    TokenSerializer,
    ResetSerializer,
    ProfileSerializer
)
from core.models import (
    TokenUser,
    Reset
)
import datetime
import random
import string
from django.db.models import Q
import requests
from django.conf import settings
from core.models import (
    Profile
)
from config.cloudinary import (
    upload_image,
    delete_image
)

import base64
from django.core.files.base import ContentFile

""" Register user for class """
class UserRegisterMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'

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

            if self.queryset.filter(email=email).exists():
                raise exceptions.APIException('Email is already registered')

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = {
                'message': 'user registered successfully'
            }

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response)

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

            # request.session['refresh_token'] = refresh_token

            # response = {
            #     'token': access_token,
            #     'success': 'successfully login'
            # }

            # return Response(response, status=status.HTTP_200_OK)

            response = Response()

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True
            )

            response.data = {
                'token': access_token,
                'success': 'successfully login',
                'status': status.HTTP_200_OK
            }

            return response
        except Exception as e:
            response = {
                "message": e.args,
                "status": status.HTTP_404_NOT_FOUND
            }
            return Response(response)

""" Refresh user token """
class RefreshMixin(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TokenSerializer
    queryset = TokenUser.objects.all()

    def create(self, request):
        try:
            # refresh_token = request.session.get('refresh_token', False)
            refresh_token = request.COOKIES.get('refresh_token', False)

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

""" logout user """
class LogoutMixin(
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TokenSerializer
    queryset = TokenUser.objects.all()
    authentication_classes = [authentication.JWTAuthentication]

    def list(self, request):
        try:
            # refresh_token = request.session.get('refresh_token', False)
            refresh_token = request.COOKIES.get('refresh_token', False)

            if not refresh_token:
                raise exceptions.AuthenticationFailed('Unauthorized User')

            self.queryset.filter(
                user=request.user.id,
                token=refresh_token
            ).delete()

            # del request.session['refresh_token']

            # response = {
            #     'message': 'Successfully logout'
            # }

            response = Response()
            response.delete_cookie('refresh_token')

            response.data = {
                'message': 'Successfully logout',
                'status': status.HTTP_200_OK
            }

            return response
        except Exception as e:
            response = {
                'message': e.args
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

""" create password reset token """
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

            token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(34))
            serializer = self.get_serializer(data={'email': email, 'token': token})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            url = 'http://localhost:5173/resetpassword/' + token

            mail = send_email(url, email)

            if mail != 1:
                self.queryset.filter(Q(email=email) & Q(token=token)).delete()
                raise exceptions.APIException("Mail not send")

            response = {
                'message': 'Check your email for reset your password',
                'status': status.HTTP_201_CREATED
            }

            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)

""" change password """
class ChangePasswordMixin(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TokenSerializer
    queryset = Reset.objects.all()

    def update(self, request, pk):
        try:
            data = request.data

            password = data.get('password', None)
            confirmpassword = data.get('confirmpassword', None)

            if password != confirmpassword:
                raise exceptions.APIException('Password and Confirm Password must be same')

            reset_password = self.queryset.filter(token=pk).first()

            if not reset_password:
                raise exceptions.APIException('Invalid link')

            user = get_user_model().objects.get(email=reset_password.email)

            if not user:
                raise exceptions.APIException('User not found')

            self.queryset.filter(Q(email=reset_password.email) & Q(token=pk)).delete()
            user.set_password(password)
            user.save()

            response = {
                'message': 'Password Successfully Reset',
                'status': status.HTTP_200_OK
            }

            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)

""" google authentication for login user """
class GoogleAuthentication(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request):
        try:
            data = request.data

            token = data.get('token', None)

            if token is None:
                raise exceptions.APIException('Invalid Credential')

            response = requests.get(
                settings.GOOGLE_USERINFO,
                params={'access_token': token['access_token']}
            )

            if not response.ok:
                raise exceptions.APIException('Invalid Credential')

            googleUser = response.json()

            user = self.queryset.filter(email=googleUser['email']).first()

            username = googleUser['name'].replace(" ", "").lower()

            if not user:
                user = self.queryset.create(
                    name = username,
                    email = googleUser['email']
                )
                user.set_password(token)
                user.save()

            access_token = authentication.create_access_token(user.id)
            refresh_token = authentication.create_refresh_token(user.id)

            TokenUser.objects.create(user=user.id, token=refresh_token)

            response = Response()

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True
            )

            response.data = {
                'token': access_token,
                'success': 'successfully login',
                'status': status.HTTP_200_OK
            }

            return response
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)

""" user details """
class ProfileMixinView(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
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

    def list(self, request):
        try:
            queryset = self.queryset.get(user=request.user)
            serializer = self.get_serializer(queryset, many=False)
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

    def update(self, request, pk):
        try:
            file = request.data.get('image', None)

            if file is None:
                raise exceptions.APIException("file field is required")

            instance = self.queryset.get(slug=pk)

            if not instance:
                raise exceptions.APIException("Invalid User")

            if instance.image:
                delete_image(instance.image)

            upload_file = upload_image(file)

            payload = {
                'image': upload_file['public_id'],
                'url': upload_file['secure_url']
            }

            serializer = self.get_serializer(
                instance,
                data=payload,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = {
                'data': 'profile picture changed successfully',
                'status': status.HTTP_200_OK
            }
            return Response(response)
        except Exception as e:
            response = {
                'message': e.args,
                'status': status.HTTP_404_NOT_FOUND
            }
            return Response(response)