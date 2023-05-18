from django.db import models

from users.models import Student
from points.models import PointsGiver


class Exam(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ('-date', )

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.title} ({self.date})"

    @property
    def parsable_date(self):
        """Date that can be parsed by front-end."""
        return self.date.strftime("%Y-%m-%d")


class ExamResult(PointsGiver):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
