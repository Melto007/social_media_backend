""" JWT tokens for authentication """

from dotenv import load_dotenv
load_dotenv()
import os
import jwt
import datetime
import requests
from django.conf import settings

from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)

from django.utils.deprecation import MiddlewareMixin

from rest_framework import exceptions
from django.contrib.auth import get_user_model

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = get_user_model().objects.get(pk=id)

            return { user, None }
        raise exceptions.AuthenticationFailed('Unauthorized User')


""" create access token """
def create_access_token(id):
    secret = os.environ['ACCESS_SECRET']

    return jwt.encode(
        {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()
        },
        secret,
        algorithm='HS256'
    )

""" decode access token """
def decode_access_token(token):
    try:
        secret = os.environ['ACCESS_SECRET']
        payload = jwt.decode(
            token,
            secret,
            algorithms='HS256'
        )

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('Unauthorized User')

""" create refresh token """
def create_refresh_token(id):
    secret = os.environ['REFERESH_SECRET']

    return jwt.encode(
        {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
        },
        secret,
        algorithm='HS256'
    )

""" decode refresh token """
def decode_refresh_token(token):
    try:
        secret = os.environ['REFERESH_SECRET']
        payload = jwt.decode(
            token,
            secret,
            algorithms='HS256'
        )

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('Unauthorized User')


# class GoogleAuthenticationMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         print("Middleware: Custom code is running!")
#         # Code to run before the view is called
#         request.foo = "bar"

#         #
#         response = self.get_response(request) #
#         return response  #

#     def google_user_info(token):
#         response = requests.get(
#             settings.GOOGLE_USERINFO,
#             params={'access_token': token['access_token']}
#         )

#         if not response.ok:
#             raise exceptions.APIException('Invalid Credential')

#         print("response", response)

#         return response.json()