from django.db import models
from django.utils import timezone
from users.models import User
from django.apps import apps


class NewsArticle(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ('-date', )

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Create action record for a new instance."""
        is_new = self.id is None
        super(NewsArticle, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'news/{self.id}',
                                                                      date=self.date,
                                                                      type='NA')
            action.save()
