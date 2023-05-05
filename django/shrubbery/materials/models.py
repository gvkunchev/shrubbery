from django.db import models
from django.utils import timezone
from users.models import User


class Material(models.Model):
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.FileField(upload_to='files')
    
    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.title} - {self.date}"
