from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
)
# from phone_field import PhoneField


def emailValidation(value):
    """ mail validation check """
    if "@gmail" in value:
        return value
    else:
        raise ValidationError("Invalid MailId")

# def phoneValidation(value):
#     """ phone validation check """
#     if len(value) == 10:
#         raise value
#     raise ValidationError("Invaild Phone Number")

class UserManager(BaseUserManager):
    """ base user manager """
    def create_user(self, email, password=None, **fields):
        """ user register """
        if not email:
            raise ValidationError("Email Field is required")

        if not password:
            raise ValidationError("Password field is required")

        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ admin create superuser """
        if not email:
            raise ValueError("Email field is required")

        if not password:
            raise ValueError("Password field is required")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """ Model for creating users """
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, validators=[emailValidation])
    password = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    username = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()


class TokenUser:
    user = models.IntegerField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.token