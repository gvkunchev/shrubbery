import os
from difflib import HtmlDiff

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.apps import apps

from challenges.models import Challenge
from users.models import User
from points.models import PointsGiver

from .pygment import pygmentize


def validate_py_extension(value):
    if not value.name.endswith('.py'):
        raise ValidationError(u'Само .py файлове са позволени.')


def get_history_upload_path(instance, filename):
    """Get history upload path based on challenge."""
    file_name = f'{instance.upload_date.strftime("%d_%m_%Y_%H_%M_%S")}.py'
    return os.path.join('challengesolutions', str(instance.challenge.pk),
                        str(instance.author.pk), file_name)


def get_upload_path(instance, filename):
    """Get latest upload path based on challenge."""
    return os.path.join('challengesolutions', str(instance.challenge.pk),
                        str(instance.author.pk), 'latest.py')


class ChallengeSolution(PointsGiver):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)
    result = models.TextField(default='')
    passed_tests = models.IntegerField(default=0)
    failed_tests = models.IntegerField(default=0)
    line_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.challenge} - {self.author}"
    
    @property
    def comments(self):
        """Get all comments."""
        return self.challengesolutioncomment_set.all()
    
    @property
    def inline_comments_count(self):
        """Get count of all inline comments."""
        return (len(ChallengeSolutionInlineComment.objects.filter(solution=self)) + 
                len(ChallengeSolutionHistoryInlineComment.objects.filter(solution=self)))

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
        self.points = round(self.challenge.points * percentage)
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
        comments = ChallengeSolutionInlineComment.objects.filter(solution=self)
        for comment in comments:
            history_comment = ChallengeSolutionHistoryInlineComment.objects.create(date=comment.date,
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
        history = ChallengeSolutionHistory.objects.create(challenge=self.challenge,
                                                         author=self.author,
                                                         upload_date=self.upload_date,
                                                         solution=self,
                                                         content=content)
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
        """Create teacher points when creating a solution."""
        is_new = self.id is None
        super(ChallengeSolution, self).save(*args, **kwargs)
        if is_new:
            teacher_points = ChallengeSolutionTeacherPoints.objects.create(solution=self)
            teacher_points.save()
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.challenge.id}/solution/{self.id}',
                                                                      date=self.upload_date,
                                                                      type='CS')
            action.save()

class ChallengeSolutionHistory(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_history_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    solution = models.ForeignKey(ChallengeSolution, on_delete=models.CASCADE)
    diff = models.TextField(default='')

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.challenge} - {self.author} - {self.upload_date}"
    
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
        super(ChallengeSolutionHistory, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.challenge.id}/solution/{self.solution.id}',
                                                                      date=timezone.now(),
                                                                      type='CSU')
            action.save()

class ChallengeSolutionComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(ChallengeSolution, on_delete=models.CASCADE)
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
        super(ChallengeSolutionComment, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments and action recording."""
        is_new = self.id is None
        super(ChallengeSolutionComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.solution.challenge.id}/solution/{self.solution.id}#comment{self.id}',
                                                                      date=self.date,
                                                                      type='CSC')
            action.save()

class ChallengeSolutionInlineComment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(ChallengeSolution, on_delete=models.CASCADE)
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
        super(ChallengeSolutionInlineComment, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.solution.challenge.id}/solution/{self.solution.id}#inlinecomment{self.id}',
                                                                      date=self.date,
                                                                      type='CSIC')
            action.save()


class ChallengeSolutionHistoryInlineComment(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey(ChallengeSolution, on_delete=models.CASCADE)
    history = models.ForeignKey(ChallengeSolutionHistory, on_delete=models.CASCADE)
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


class ChallengeSolutionTeacherPoints(PointsGiver):

    solution = models.OneToOneField(ChallengeSolution, on_delete=models.CASCADE)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.solution} - {self.points}"
