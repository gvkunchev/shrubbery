from django.db import models
from django.contrib.auth.models import AbstractUser
from .model_managers import UserManager


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Student(User):
    """Student model."""
    fn = models.CharField(max_length=100)
    REQUIRED_FIELDS = User.REQUIRED_FIELDS + ['fn']

    class Meta:
        verbose_name = "Student"


class Teacher(User):
    """Teacher model."""

    class Meta:
        verbose_name = "Teacher"
