from django.db import models
from users.models import User


class Material(models.Model):
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.FileField(upload_to='materials')

    class Meta:
        ordering = ('date', 'title')

    @property
    def parsable_date(self):
        """Date that can be parsed by front-end."""
        return self.date.strftime("%Y-%m-%d")
    
    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.title} - {self.date}"
