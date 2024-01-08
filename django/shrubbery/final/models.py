from django.db import models
from django.utils import timezone

from users.models import Student


class FinalScheduleSlot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    students = models.ManyToManyField(Student, blank=True)

    class Meta:
        ordering = ('start',)

    def human_time(self):
        """Return start-end as human readable string."""
        start = self.start.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y (%H:%M")
        end = self.end.astimezone(timezone.get_current_timezone()).strftime("%H:%M)")
        return f'{start} - {end}'

    @property
    def parsable_start(self):
        """Deadline that can be parsed by front-end."""
        return self.start.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")

    @property
    def parsable_end(self):
        """Deadline that can be parsed by front-end."""
        return self.end.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")
    

class FinalExchange(models.Model):
    requester = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL, related_name='exchange_requests')
    confirmer = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL, related_name='exchange_confirmations')
