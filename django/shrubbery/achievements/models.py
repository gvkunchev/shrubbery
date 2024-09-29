from django.db import models

from points.models import PointsGiver
from users.models import Student



class Achievement(PointsGiver):

    owner = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    achieved = models.BooleanField(default=False)

    class Meta:
        abstract = True


class KingArthur(Achievement):
    NAME = 'King Arthur'
    DESCRIPTION = 'Постигнати най-много точки от контролно/изпит'
    IMAGE = 'king_arthur.png'
    POINTS = 1


# Update this so that all other apps know the complete list of achevements
ACHIEVEMENTS = (KingArthur, )
