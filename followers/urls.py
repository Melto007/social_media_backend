from django.urls import (
    path,
    include
)
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register("findFollowers", views.FollowersViewSet, basename="findFollowers")
router.register('following', views.FollowingViewSet, basename='following')

urlpatterns = [
    path("", include(router.urls))
]
