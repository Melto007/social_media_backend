from . import views
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('post', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls))
]
