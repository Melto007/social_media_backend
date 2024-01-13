from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()

router.register('register', views.UserRegisterMixin, basename='register')
router.register('login', views.LoginMixin, basename='login')

urlpatterns = [
    path('', include(router.urls))
]
