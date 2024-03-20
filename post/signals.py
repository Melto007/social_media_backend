from django.db.models.signals import (
    pre_save
)
from django.dispatch import receiver
from core.models import (
    Tag,
    Post
)

@receiver(pre_save, sender=Post)
def pre_save_tag(sender, instance, **kwargs):
    print(instance, instance.tag)