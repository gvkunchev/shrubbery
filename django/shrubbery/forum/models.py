from django.db import models
from django.utils import timezone
from users.models import User

from points.models import PointsGiver


class Forum(models.Model):
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

    @property
    def comments(self):
        """Get all comments."""
        return self.forumcomment_set.all()
    
    @property
    def latest_comment(self):
        """Get last comment."""
        return self.forumcomment_set.first()


class ForumComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    starred = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date', )

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date}"

    def _update_points(self):
        """Update points assigned if starred."""
        if self.starred:
            self.points = 1
        else:
            self.points = 0

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments."""
        super(ForumComment, self).save(*args, **kwargs)
        self._update_points()
