import os
from uuid import uuid4

from PIL import Image

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
    image = models.ImageField(upload_to=rename_profile_picture, blank=True)
    github = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        """Get full name."""
        return f"{self.first_name} {self.last_name}"

    def _resize_image(self):
        """Resize profile picture on upload."""
        width = 250
        height = 250

        img = Image.open(self.image.path)
        original_aspect = img.width/img.height
        thumbnail_aspect = width/height
        
        if original_aspect == thumbnail_aspect:
            # return resized image
            thumb = img.resize((width, height))
        else:
            # create transparent background size of requested thumbnail
            thumb = Image.new('RGB', (width, height), (255, 255, 255)) 
            thumb.putalpha(0)

            if thumbnail_aspect < original_aspect:
            # thumb aspect ratio is more narrow than original
                # scale as proportion of width
                resized_original = img.resize((width, round(img.height * width/img.width)))
                # paste into background with top/bottom spacing
                thumb.paste(resized_original, (0, (height-resized_original.height)//2))
            else:
            # thumb aspect ratio is wider than original
                # scale as proportion of height
                resized_original = img.resize((round(img.width * height/img.height), height))
                # paste into background with left/right spacing
                thumb.paste(resized_original, ((width-resized_original.width)//2, 0))
        thumb.save(self.image.path)

    def save(self, *args, **kwargs):
        """Clean up on save."""
        old_image = self.image.path if self.image else None
        super().save(args, kwargs)
        new_image = self.image.path if self.image else None
        if new_image and old_image != new_image:
            self._resize_image()


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
