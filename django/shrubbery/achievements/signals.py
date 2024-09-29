from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from users.models import Student
from exams.models import Exam, ExamResult
from .models import ACHIEVEMENTS, KingArthur



@receiver(post_save, sender=Student) 
def create_achievements(sender, instance, created, **kwargs):
    """Initiate empty achievements when creating a Student."""
    if not created: # Modifying old instance - nothing to do
        return
    for achievement in ACHIEVEMENTS:
        achievement.objects.create(owner=instance)


def update_king_arthurs_achievement():
    """Update all King Arthurs achievements"""
    # Collect max score for every exam
    exam_max_scores = {}
    for exam in Exam.objects.all():
        max_score = 0
        if len(exam.examresult_set.values()):
            max_score = max(map(lambda x: x['points'], exam.examresult_set.values()))
        exam_max_scores[exam.pk] = max_score
    # Set achievement based on max scores in all exams
    for user in Student.objects.all():
        # Assume not achieved
        achieved = False
        # Look for an exam that gives the achievement
        for exam in Exam.objects.all():
            try:
                if exam.examresult_set.get(owner=user).points == exam_max_scores[exam.pk]:
                    achieved = True
                    break
            except ObjectDoesNotExist:
                continue # No exam result for this user in this exam -> go to next exam
        # Set achievement status to the database
        if achieved:
            achievement = KingArthur.objects.get(owner=user)
            achievement.achieved = True
            achievement.points = KingArthur.POINTS
            achievement.save()
        else:
            achievement = KingArthur.objects.get(owner=user)
            achievement.achieved = False
            achievement.points = 0
            achievement.save()

@receiver(post_save, sender=ExamResult) 
def post_save_exam_results(*args, **kwargs):
    update_king_arthurs_achievement()

@receiver(post_delete, sender=ExamResult) 
def post_delete_exam_results(*args, **kwargs):
    update_king_arthurs_achievement()

@receiver(post_save, sender=Exam) 
def post_save_exam(*args, **kwargs):
    update_king_arthurs_achievement()

@receiver(post_delete, sender=Exam) 
def post_delete_exam(*args, **kwargs):
    update_king_arthurs_achievement()
