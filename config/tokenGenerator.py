from .authentication import (
    create_access_token,
    create_refresh_token
)
from core.models import TokenUser
from rest_framework.response import Response
from rest_framework import status

def tokenGenerator(user):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    TokenUser.objects.create(user=user, token=refresh_token)

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