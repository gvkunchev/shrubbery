from django.db import models


class PointsGiver(models.Model):

    points = models.IntegerField(default=0)

    class Meta:
        abstract = True
