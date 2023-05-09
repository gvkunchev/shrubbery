from django.db import models


class ProfilePicture(models.ImageField):
    """User's profile picture."""

    def clean(self, file, user):
        return file
        