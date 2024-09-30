import os
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from users.models import Student
from exams.models import Exam, ExamResult
from homeworks.models import Homework
from homeworksolutions.models import HomeworkSolution
from .models import ACHIEVEMENTS, KingArthur, SirBedevere


def background_process(fun):
    """Decorator for running on the background only if celery is present."""
    def wrapped(*args, **kwargs):
        if os.environ.get('SHRUBBERY_ENV') == 'prd':
            fun.delay(*args, **kwargs)
        else:
            fun(*args, **kwargs)
    return wrapped


@receiver(post_save, sender=Student) 
def create_achievements(sender, instance, created, **kwargs):
    """Initiate empty achievements when creating a Student."""
    if not created: # Modifying old instance - nothing to do
        return
    for achievement in ACHIEVEMENTS:
        achievement.objects.create(owner=instance)


@background_process
@shared_task
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
        KingArthur.objects.get(owner=user).toggle(achieved)

@receiver(post_save, sender=ExamResult) 
def post_save_exam_results(*args, **kwargs):
    update_king_arthurs_achievement()

@receiver(post_delete, sender=ExamResult) 
def post_delete_exam_results(*args, **kwargs):
    update_king_arthurs_achievement()



@background_process
@shared_task
def update_sir_bedevere_achievement(user):
    """Update all Sir Bedevere achievements."""
    if user.is_teacher:
        return
    achieved = False
    try:
        solutions = HomeworkSolution.objects.filter(author=user, homework__verified=True)
        for solution in solutions:
            if solution.points >= (solution.homework.points * 8) / 10:
                source_code = os.path.join(settings.MEDIA_ROOT, solution.content.path)
                used_lines = 0
                with open(source_code) as f:
                    for line in f.readlines():
                        if line.strip():
                            used_lines += 1
                if used_lines <= 4:
                    achieved = True
                    break
    except ObjectDoesNotExist:
        pass # No exam result for this user in this exam -> go to next exam
    SirBedevere.objects.get(owner=user).toggle(achieved)

@receiver(post_save, sender=HomeworkSolution) 
def post_save_homework_solution(sender, instance, **kwargs):
    update_sir_bedevere_achievement(instance.author)

@receiver(post_delete, sender=HomeworkSolution) 
def post_delete_homework_solution(sender, instance, **kwargs):
    update_sir_bedevere_achievement(instance.author)

@receiver(post_save, sender=Homework) 
def post_save_homework(sender, instance, **kwargs):
    for solution in instance.homeworksolution_set.all():
        update_sir_bedevere_achievement(solution.author)


