from django.db import models
from django.utils import timezone

from users.models import User
from points.models import PointsGiver


class Homework(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    points = models.IntegerField(default=10)
    sanity_test = models.TextField(default="", null=True, blank=True)
    full_test = models.TextField(default="", null=True, blank=True)
    hidden = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    executing_tests = models.BooleanField(default=False)

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return self.title
    
    @property
    def can_upload(self):
        """Whether solutions can be uploaded or not."""
        if self.hidden:
            return False
        if self.verified:
            return False
        if self.deadline < timezone.now():
            return False
        return True

    @property
    def comments(self):
        """Get all comments."""
        return self.homeworkcomment_set.all()

    @property
    def human_deadline(self):
        """Deadline format for human readers.."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    @property
    def parsable_deadline(self):
        """Deadline that can be parsed by front-end."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")


class HomeworkComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
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

    def _update_points(self, *args, **kwargs):
        """Update points assigned if starred."""
        if self.starred:
            self.points = 1
        else:
            self.points = 0
        super(HomeworkComment, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments."""
        super(HomeworkComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
