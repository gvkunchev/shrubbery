import os
from difflib import HtmlDiff

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.apps import apps

from homeworks.models import Homework
from users.models import User, Teacher
from points.models import PointsGiver

from .pygment import pygmentize


def validate_py_extension(value):
    if not value.name.endswith('.py'):
        raise ValidationError(u'Само .py файлове са позволени.')


def get_history_upload_path(instance, filename):
    """Get history upload path based on homework."""
    file_name = f'{instance.upload_date.strftime("%d_%m_%Y_%H_%M_%S")}.py'
    return os.path.join('homeworksolutions', str(instance.homework.pk),
                        str(instance.author.pk), file_name)


def get_upload_path(instance, filename):
    """Get latest upload path based on homework."""
    return os.path.join('homeworksolutions', str(instance.homework.pk),
                        str(instance.author.pk), 'latest.py')


class HomeworkSolution(PointsGiver):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    result = models.TextField(default='')
    passed_tests = models.IntegerField(default=0)
    failed_tests = models.IntegerField(default=0)
    line_count = models.IntegerField(default=0)
    subscribers = models.ManyToManyField(Teacher, related_name='subscribed_homeworks', blank=True)
    commit_message = models.TextField(default='', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.homework} - {self.author}"
    
    @property
    def comments(self):
        """Get all comments."""
        return self.homeworksolutioncomment_set.all()
    
    @property
    def inline_comments_count(self):
        """Get count of all inline comments."""
        return (len(HomeworkSolutionInlineComment.objects.filter(solution=self)) + 
                len(HomeworkSolutionHistoryInlineComment.objects.filter(solution=self)))

    def assign_line_count(self, *args, **kwargs):
        """Assign line count to the database."""
        with open(os.path.join(settings.MEDIA_ROOT, self.content.path)) as f:
            self.line_count = len(f.readlines())
            self.save()

    def assign_points(self):
        """Assign points based on the result."""
        total = self.passed_tests + self.failed_tests
        if total == 0:
            return False
        percentage = self.passed_tests / total
        self.points = round(self.homework.points * percentage)
        self.save()
    
    def _reset_points(self):
        """Reset points when sending to history."""
        self.upload_date = timezone.now()
        self.result = ''
        self.passed_tests = 0
        self.failed_tests = 0
        self.points = 0
        self.save()
    
    def _send_inline_comments_to_history(self, history):
        """Send inline comments to history."""
        comments = HomeworkSolutionInlineComment.objects.filter(solution=self)
        for comment in comments:
            history_comment = HomeworkSolutionHistoryInlineComment.objects.create(date=comment.date,
                                                                                  author=comment.author,
                                                                                  solution=comment.solution,
                                                                                  history=history,
                                                                                  content=comment.content,
                                                                                  line=comment.line)
            history_comment.save()
            comment.delete()

    def send_to_history(self):
        """Send current version to history."""
        content = get_history_upload_path(self, None)
        os.rename(os.path.join(settings.MEDIA_ROOT, self.content.path),
                  os.path.join(settings.MEDIA_ROOT, content))
        history = HomeworkSolutionHistory.objects.create(homework=self.homework,
                                                         author=self.author,
                                                         upload_date=self.upload_date,
                                                         solution=self,
                                                         content=content,
                                                         commit_message=self.commit_message)
        history.save()
        self._reset_points()
        self._send_inline_comments_to_history(history)
        return history

    def get_content(self):
        """Get content from a solution file."""
        try:
            with open(os.path.join(settings.MEDIA_ROOT, self.content.path)) as f:
                return pygmentize(f.read())
        except:
            return "Грешка при четене на файла с решение."

    @property
    def human_upload_date(self):
        """Ipload date format for human readers.."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def save(self, *args, **kwargs):
        """Create teacher points when creating a solution and create an action record."""
        is_new = self.id is None
        super(HomeworkSolution, self).save(*args, **kwargs)
        if is_new:
            teacher_points = HomeworkSolutionTeacherPoints.objects.create(solution=self)
            teacher_points.save()
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'homework/{self.homework.id}/solution/{self.id}',
                                                                      date=self.upload_date,
                                                                      type='HWS')
            action.save()

    def is_followed_up_by_teacher(self):
        """Is there any comment to the solution from a teacher after this version of the solution?"""
        for comment in self.comments:
            if comment.date > self.upload_date:
                if comment.author.is_teacher():
                    return True
        for comment in HomeworkSolutionInlineComment.objects.filter(solution=self):
            if comment.date > self.upload_date:
                if comment.author.is_teacher():
                    return True
        return False
    
    def has_history(self):
        """If homework solution already has history."""
        return len(HomeworkSolutionHistory.objects.filter(solution=self))
    
    def has_history_after(self, date):
        """If has history after a given date."""
        for history in HomeworkSolutionHistory.objects.filter(solution=self):
            if history.upload_date > date:
                return True
        return False

class HomeworkSolutionHistory(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_history_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    solution = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)
    diff = models.TextField(default='')
    commit_message = models.TextField(default='', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.homework} - {self.author} - {self.upload_date}"
    
    def assign_diff_to(self, target):
        """Generate diff of current solution to target and store it."""
        differ = HtmlDiff()
        with open(os.path.join(settings.MEDIA_ROOT, self.content.path)) as f:
            old = f.readlines()
        with open(os.path.join(settings.MEDIA_ROOT, target.content.path)) as f:
            new = f.readlines()
        self.diff = ''.join(differ.make_file(old, new))
        self.save()
        
    @property
    def human_upload_date(self):
        """Ipload date format for human readers.."""
        return self.upload_date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")
    
    def save(self, *args, **kwargs):
        """Create action record for a new instance."""
        is_new = self.id is None
        super(HomeworkSolutionHistory, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'homework/{self.homework.id}/solution/{self.solution.id}',
                                                                      date=timezone.now(),
                                                                      type='HWSU')
            action.save()


class HomeworkSolutionComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)
    content = models.TextField()
    starred = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date', )

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date}"

    def _update_points(self, *args, **kwargs):
        """Update points assigned if starred."""
        if self.starred:
            self.points = 1
        else:
            self.points = 0
        super(HomeworkSolutionComment, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments and action recording."""
        is_new = self.id is None
        super(HomeworkSolutionComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'homework/{self.solution.homework.id}/solution/{self.solution.id}#comment{self.id}',
                                                                      date=self.date,
                                                                      type='HWSC')
            action.save()

    def is_followed_up_by_teacher(self):
        """Is there any comment to the solution from a teacher after this comment?"""
        for comment in self.solution.comments:
            if comment.date > self.date:
                if comment.author.is_teacher():
                    return True
        for comment in HomeworkSolutionInlineComment.objects.filter(solution=self.solution):
            if comment.date > self.date:
                if comment.author.is_teacher():
                    return True
        return False

class HomeworkSolutionInlineComment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)
    content = models.TextField()
    line = models.IntegerField()

    class Meta:
        ordering = ('line', 'date')

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date}"

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments and action recording."""
        is_new = self.id is None
        super(HomeworkSolutionInlineComment, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'homework/{self.solution.homework.id}/solution/{self.solution.id}#inlinecomment{self.id}',
                                                                      date=self.date,
                                                                      type='HWSIC')
            action.save()

    def is_followed_up_by_teacher(self):
        """Is there any comment to the solution from a teacher after this comment?"""
        for comment in self.solution.comments:
            if comment.date > self.date:
                if comment.author.is_teacher():
                    return True
        for comment in HomeworkSolutionInlineComment.objects.filter(solution=self.solution):
            if comment.date > self.date:
                if comment.author.is_teacher():
                    return True
        return False


class HomeworkSolutionHistoryInlineComment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)
    history = models.ForeignKey(HomeworkSolutionHistory, on_delete=models.CASCADE)
    content = models.TextField()
    line = models.IntegerField()

    class Meta:
        ordering = ('line', 'date')

    @property
    def human_date(self):
        """Date format used for parsing templates."""
        return self.date.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.author} - {self.human_date}"


class HomeworkSolutionTeacherPoints(PointsGiver):

    solution = models.OneToOneField(HomeworkSolution, on_delete=models.CASCADE)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.solution} - {self.points}"
