from django.db import models


class PointsGiver(models.Model):

    points = models.IntegerField()

    class Meta:
        abstract = True 
