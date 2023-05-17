import os
from uuid import uuid4

from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

from .model_managers import UserManager

from points.models import PointsGiver


def rename_profile_picture(instance, filename):
    upload_to = 'profiles'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}.{ext}'
    else:
        while os.path.exists(os.path.join(upload_to, filename)):
            filename = f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)


class ProfilePicturePoints(PointsGiver):

    owner = models.ForeignKey('Student', on_delete=models.CASCADE)


class User(AbstractUser):
    """User model."""

    class Meta:
        ordering = ('is_active', 'first_name', 'last_name')

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=rename_profile_picture, blank=True)
    github = models.CharField(max_length=100, blank=True)
    dark_theme = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def is_teacher(self):
        return Teacher.objects.filter(email=self.email).exists()

    @property
    def is_student(self):
        return Student.objects.filter(email=self.email).exists()

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
            if self.image.path.endswith('.png'):
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
    
    def _update_profile_picture_points(self):
        """Assign or remove points based on profile picture existence."""
        if not self.is_student:
            return False
        if self.image:
            try:
                # User already has points - no action needed
                ProfilePicturePoints.objects.get(owner=self)
            except ObjectDoesNotExist:
                # User has no points yet - assign points
                owner = Student.objects.get(pk=self.pk)
                ProfilePicturePoints.objects.create(owner=owner, points=1)
        else:
            try:
                # User has points - remove them
                profile_picture_points = ProfilePicturePoints.objects.get(owner=self)
                profile_picture_points.delete()
            except ObjectDoesNotExist:
                pass # User have no points anyway

    def save(self, *args, **kwargs):
        """Decorate saving with cleanup and points assignments."""
        old_image = self.image.path if self.image else None
        super(User, self).save(*args, **kwargs)
        new_image = self.image.path if self.image else None
        if new_image and old_image != new_image:
            self._resize_image()
        self._update_profile_picture_points()


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
