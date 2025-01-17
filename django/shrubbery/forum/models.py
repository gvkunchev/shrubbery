from django.db import models
from django.utils import timezone
from django.apps import apps
from users.models import User
from shrubbery.easter_eggs import decorate_with_youtube
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
        return f"{self.title} - {self.author} - {self.human_date}"

    @property
    def comments(self):
        """Get all comments."""
        return self.forumcomment_set.all()

    @property
    def latest_comment(self):
        """Get last comment."""
        return self.forumcomment_set.first()

    def save(self, *args, **kwargs):
        """Create action record for a new instance."""
        is_new = self.id is None
        self.content = decorate_with_youtube(self.content)
        super(Forum, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'forum/{self.id}',
                                                                      date=self.date,
                                                                      type='F')
            action.save()

class ForumComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    starred = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-date', )

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date}"

    def _update_points(self, *args, **kwargs):
        """Update points assigned if starred."""
        if self.starred:
            self.points = 1
        else:
            self.points = 0
        super(ForumComment, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments and an action record."""
        is_new = self.id is None
        self.content = decorate_with_youtube(self.content)
        super(ForumComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'forum/{self.forum.id}#comment{self.id}',
                                                                      date=self.date,
                                                                      type='FC')
            action.save()

    def is_answered_by_teacher(self):
        """Is there an answer to the forum from a teacher after this comment?"""
        for comment in self.forum.comments:
            if comment.date > self.date:
                if (comment.parent is None and self.parent is None) or comment.parent == self.parent or comment.parent == self:
                    if comment.author.is_teacher():
                        return True
        return False
