from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
)
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse


def emailValidation(value):
    """ mail validation check """
    if "@gmail" in value:
        return value
    else:
        raise ValidationError("Invalid MailId")

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


class TokenUser(models.Model):
    user = models.IntegerField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=settings.TOKEN_EXPIRES)

    def __str__(self):
        return str(self.token)


class Reset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.name)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.name)
        return super().save(*args, **kwargs)

class ProfileDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    county = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.name)

class Follower(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    userProfile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="userProfile"
    )
    status = models.BooleanField(default=True)

    def __str__(self):
        names = self.user.name + ' is following ' + self.following.name
        return str(names)

class Tag(models.Model):
    tags = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.tags)

class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.DO_NOTHING,
        related_name='tag',
        null=True,
        blank=True
    )
    post = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.profile.user.name

class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    image = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.profile.user.name