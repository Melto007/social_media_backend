from django.contrib import admin
from core import models

admin.site.register(models.User)
admin.site.register(models.TokenUser)
admin.site.register(models.Reset)