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


class SirBedevere(Achievement):
    NAME = 'Sir Bedevere'
    DESCRIPTION = 'Домашно с поне 80% точки от тестове и написано на не повече от 4 реда'
    IMAGE = 'sir_bedevere.png'
    POINTS = 1


class SirLancelot(Achievement):
    NAME = 'Sir Lancelot'
    DESCRIPTION = 'Първа версия на домашно, предадена в последните 30 секунди преди крайния срок'
    IMAGE = 'sir_lancelot.png'
    POINTS = 1


# Update this so that all other apps know the complete list of achevements
ACHIEVEMENTS = (KingArthur, SirBedevere, SirLancelot)
