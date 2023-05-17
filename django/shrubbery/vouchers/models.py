from django.db import models
from django.utils import timezone

from points.models import PointsGiver
from users.models import Student


class Voucher(PointsGiver):

    owner = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    token = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('owner', 'date')

    def update_date(self):
        """Update date on redeeming."""
        self.date = timezone.now()

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return self.token
