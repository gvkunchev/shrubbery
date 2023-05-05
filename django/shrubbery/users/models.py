import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from .model_managers import UserManager


def rename_profile_picture(instance, filename):
    upload_to = 'profiles'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}.{ext}'
    else:
        while os.path.exists(os.path.join(upload_to, filename)):
            filename = f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)
    

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=rename_profile_picture)
    github = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        """Get full name."""
        return f"{self.first_name} {self.last_name}"


class Student(User):
    """Student model."""
    fn = models.CharField(max_length=100, unique=True)
    REQUIRED_FIELDS = User.REQUIRED_FIELDS + ['fn']

    class Meta:
        verbose_name = "Student"


class Teacher(User):
    """Teacher model."""

    class Meta:
        verbose_name = "Teacher"
