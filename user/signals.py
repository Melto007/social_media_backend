from core.models import (
    Profile,
    ProfileDetails
)
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=get_user_model())
def post_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        ProfileDetails.objects.create(user=instance)
