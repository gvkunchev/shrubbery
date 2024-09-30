from django.db import models

from points.models import PointsGiver
from users.models import Student



class Achievement(PointsGiver):

    owner = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    achieved = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
    def toggle(self, achieved):
        """Toggle status based on input bool."""
        if achieved:
            self.achieved = True
            self.points = KingArthur.POINTS
            self.save()
        else:
            self.achieved = False
            self.points = 0
            self.save()


class BiggusDickus(Achievement):
    NAME = 'Biggus Dickus'
    DESCRIPTION = 'TODO'
    HINT = 'TODO'
    IMAGE = 'TODO.png'
    POINTS = 1


class BlackKnight(Achievement):
    NAME = 'Black Knight'
    DESCRIPTION = 'Домашно с 8 или повече предадени ревизии'
    HINT = 'Важното е човек никога да не се отказва'
    IMAGE = 'TODO.png'
    POINTS = 1


class Bors(Achievement):
    NAME = 'Bors'
    DESCRIPTION = 'Домашно предадено до час след публикуването му с поне 50% точки от тестовете'
    HINT = 'В чест на най-скоростно загиналия рицар от Кръглата Маса'
    IMAGE = 'TODO.png'
    POINTS = 1


class BraveSirRobin(Achievement):
    NAME = 'Brave Sir Robin'
    DESCRIPTION = 'Добавен github акаунт'
    HINT = 'Ще се пеят истории за вас, стига бардовете да имат достатъчно за разказване'
    IMAGE = 'TODO.png'
    POINTS = 1


class BrianCohen(Achievement):
    NAME = 'Brian Cohen'
    DESCRIPTION = 'Качена снимка в сайта'
    HINT = 'Всичко трябва да започне от някъде'
    IMAGE = 'TODO.png'
    POINTS = 1


class Bridgekeeper(Achievement):
    NAME = 'Bridgekeeper'
    DESCRIPTION = '3 успешно решени предизвикателства'
    HINT = 'Всички отговори трябва да са верни'
    IMAGE = 'TODO.png'
    POINTS = 1


class Concorde(Achievement):
    NAME = 'Concorde'
    DESCRIPTION = '2 или повече отнети точки на домашни или предизвикателства'
    HINT = 'Раната не е фатална, но си вземете поука'
    IMAGE = 'TODO.png'
    POINTS = 1


class DeadCollector(Achievement):
    NAME = 'Dead collector'
    DESCRIPTION = 'Домашно (ревизия) с 5 или повече импортирани модула'
    HINT = 'Събирайте мъртъвци на воля!'
    IMAGE = 'TODO.png'
    POINTS = 1


class FrenchTaunter(Achievement):
    NAME = 'French Taunter'
    DESCRIPTION = 'Домашно с 8 или повече коментара в кода'
    HINT = 'I fart in your general direction'
    IMAGE = 'TODO.png'
    POINTS = 1


class Gawain(Achievement):
    NAME = 'Gawain'
    DESCRIPTION = 'TODO'
    HINT = 'TODO'
    IMAGE = 'TODO.png'
    POINTS = 1


class HolyHandGrenadeOfAntioch(Achievement):
    NAME = 'Holy Hand Grenade of Antioch'
    DESCRIPTION = '2 предадени домашни с 0 точки'
    HINT = '"[...] neither count thou two, excepting that thou then proceed to three."'
    IMAGE = 'TODO.png'
    POINTS = 3


class KingArthur(Achievement):
    NAME = 'King Arthur'
    DESCRIPTION = 'Постигнати най-много точки от контролно/изпит'
    HINT = 'Може да има само един крал... На контролно...'
    IMAGE = 'TODO.png'
    POINTS = 1


class KnightsWhoSayNi(Achievement):
    NAME = 'Knights who say Ni'
    DESCRIPTION = '8 или повече написани коментара в сайта (домашни, предизвикателства, форум)'
    HINT = 'Ни! Ни! Ни!... И така нататък...'
    IMAGE = 'TODO.png'
    POINTS = 1


class PontiusPilate(Achievement):
    NAME = 'Pontius Pilate'
    DESCRIPTION = 'Домашно или предизвикателство без употребата на буквата "r"'
    HINT = 'Wome... is your fwiend!'
    IMAGE = 'TODO.png'
    POINTS = 1


class RabbitOfCaerbannog(Achievement):
    NAME = 'Rabbit of Caerbannog'
    DESCRIPTION = 'Отключени (почти) всички ачийвмънти'
    HINT = 'TODO'
    IMAGE = 'TODO.png'
    POINTS = 5


class SirBedevere(Achievement):
    NAME = 'Sir Bedevere'
    DESCRIPTION = '5 или повече предадени домашни'
    HINT = 'Единственият рицар от Кръглата Маса, който оцелява до края'
    IMAGE = 'TODO.png'
    POINTS = 1


class SirEctor(Achievement):
    NAME = 'Sir Ector'
    DESCRIPTION = 'TODO'
    HINT = 'TODO'
    IMAGE = 'TODO.png'
    POINTS = 1


class SirGalahad(Achievement):
    NAME = 'Sir Galahad'
    DESCRIPTION = '6 предадени предизвикателства'
    HINT = 'Има само 150 от тях, можете да ги победите'
    IMAGE = 'TODO.png'
    POINTS = 1


class SirLancelot(Achievement):
    NAME = 'Sir Lancelot'
    DESCRIPTION = 'Домашно предадено 30 секунди преди крайния срок'
    HINT = 'Сър Ланселот е най-смелият член на Кръглата Маса'
    IMAGE = 'TODO.png'
    POINTS = 1


class TheSpanishInquisition(Achievement):
    NAME = 'The Spanish Inquisition'
    DESCRIPTION = 'Домашно предадено в час, сборът на чиито цифри е равен на 69'
    HINT = 'Никой не очаква Испанската Инквизиция!'
    IMAGE = 'TODO.png'
    POINTS = 1


class ThreeHeadedGiant(Achievement):
    NAME = 'Three-Headed Giant'
    DESCRIPTION = 'TODO'
    HINT = 'TODO'
    IMAGE = 'TODO.png'
    POINTS = 1


class TimTheEnchanter(Achievement):
    NAME = 'Tim the Enchanter'
    DESCRIPTION = 'Домашно с поне 80% точки от тестове и написано на не повече от 4 реда'
    HINT = 'Колко магически код би написал Тим?'
    IMAGE = 'TODO.png'
    POINTS = 1


# Update this so that all other apps know the complete list of achevements
ACHIEVEMENTS = (BiggusDickus, BlackKnight, Bors, BraveSirRobin,
                BrianCohen, Bridgekeeper, Concorde,
                DeadCollector, FrenchTaunter, Gawain,
                HolyHandGrenadeOfAntioch, KingArthur,
                KnightsWhoSayNi, PontiusPilate,
                RabbitOfCaerbannog, SirBedevere,
                SirEctor, SirGalahad, SirLancelot,
                TheSpanishInquisition, ThreeHeadedGiant,
                TimTheEnchanter)
