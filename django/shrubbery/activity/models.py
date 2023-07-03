from django.db import models
from users.models import User
from django.utils import timezone

# Improting the monitor to get it registered on start-up
from . import signal_monitor


class Action(models.Model):

    class Meta:
        ordering = ('-date', )

    class ActionType(models.TextChoices):
        NEWS_ARTICLE = 'NA', 'News Article'
        FORUM = 'F', 'Forum'
        FORUM_COMMENT = 'FC', 'Forum Comment'
        HOMEWORK = 'HW', 'Homework'
        HOMEWORK_COMMENT = 'HWC', 'Homework Comment'
        HOMEWORK_SOLUTION = 'HWS', 'Homework Solution'
        HOMEWORK_SOLUTION_UPDATE = 'HWSU', 'Homework Solution Update'
        HOMEWORK_SOLUTION_COMMENT = 'HWSC', 'Homework Solution Comment'
        HOMEWORK_SOLUTION_INLINE_COMMENT = 'HWSIC', 'Homework Solution Inline Comment'
        CHALLENGE = 'C', 'Challenge'
        CHALLENGE_COMMENT = 'CC', 'Challenge Comment'
        CHALLENGE_SOLUTION = 'CS', 'Challenge Solution'
        CHALLENGE_SOLUTION_UPDATE = 'CSU', 'Challenge Solution Update'
        CHALLENGE_SOLUTION_COMMENT = 'CSC', 'Challenge Solution Comment'


    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    link = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(
        max_length=5,
        choices=ActionType.choices,
        default=None, blank=True, null=True
    )

    @property
    def human_date(self):
        """Date format for human readers.."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M:%S")
