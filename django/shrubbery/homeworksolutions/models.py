import os

from django.db import models
from django.utils import timezone

from homeworks.models import Homework
from users.models import User
from points.models import PointsGiver


def get_upload_path(instance, filename):
    """Get upload path bsaed on homework."""
    return os.path.join('solutions', str(instance.homework.pk),
                        str(instance.author.pk), 'latest.py')


class HomeworkSolution(PointsGiver):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_upload_path)
    upload_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.homework} - {self.author} - {self.upload_date}"

    @property
    def human_upload_date(self):
        """Ipload date format for human readers.."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")
