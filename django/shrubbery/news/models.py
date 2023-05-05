from django.db import models
from django.utils import timezone
from users.models import User


class NewsArticle(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    content = models.TextField()

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.strftime("%d.%m.%Y %H:%M")
    
    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date} - {self.title}"
