from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from authentication.utils import get_upload_path_user


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=60, null=True, blank=True)  # Combined name field
    avatar = models.ImageField(
        default="default.png",
        upload_to=get_upload_path_user,
    )
    type = models.IntegerField(choices=[(1, 1), (2, 2)], default=1)
    open_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        unique=True,
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[
                0
            ]  # Generate a username based on the email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
