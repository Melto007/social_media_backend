from django.contrib import admin
from core import models

admin.site.register(models.User)
admin.site.register(models.TokenUser)
admin.site.register(models.Reset)
admin.site.register(models.Profile)
admin.site.register(models.ProfileDetails)
admin.site.register(models.Follower)
admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.PostImage)