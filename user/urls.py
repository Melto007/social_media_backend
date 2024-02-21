from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from user import views

router = DefaultRouter()

router.register('register', views.UserRegisterMixin, basename='register')
router.register('login', views.LoginMixin, basename='login')
router.register('profile', views.ProfileMixinView, basename='profile')
router.register('refresh', views.RefreshMixin, basename='refresh')
router.register('logout', views.LogoutMixin, basename='logout')
router.register('reset', views.ResetMixin, basename='reset')
router.register('change-password', views.ChangePasswordMixin, basename='change-password')
router.register('google-auth', views.GoogleAuthentication, basename='google-auth')

urlpatterns = [
    path('', include(router.urls)),
]
