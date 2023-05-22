import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from homeworks.models import Homework
from users.models import User
from points.models import PointsGiver

from .pygment import pygmentize


def validate_py_extension(value):
    if not value.name.endswith('.py'):
        raise ValidationError(u'Само .py файлове са позволени.')


def get_history_upload_path(instance, filename):
    """Get history upload path based on homework."""
    file_name = f'{instance.upload_date.strftime("%d_%m_%Y_%H_%M_%S")}.py'
    return os.path.join('solutions', str(instance.homework.pk),
                        str(instance.author.pk), file_name)


def get_upload_path(instance, filename):
    """Get latest upload path based on homework."""
    return os.path.join('solutions', str(instance.homework.pk),
                        str(instance.author.pk), 'latest.py')


class HomeworkSolution(PointsGiver):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.homework} - {self.author}"
    
    @property
    def comments(self):
        """Get all comments."""
        return self.homeworksolutioncomment_set.all()
    
    def send_to_history(self):
        """Send current version to history."""
        content = get_history_upload_path(self, None)
        os.rename(os.path.join(settings.MEDIA_ROOT, self.content.path),
                  os.path.join(settings.MEDIA_ROOT, content))
        history = HomeworkSolutionHistory.objects.create(homework=self.homework,
                                                         author=self.author,
                                                         upload_date=self.upload_date,
                                                         solution=self,
                                                         content=content)
        history.save()
        self.upload_date = timezone.now()
        self.save()

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


class HomeworkSolutionHistory(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(upload_to=get_history_upload_path, validators=[validate_py_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    solution = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return f"{self.homework} - {self.author} - {self.upload_date}"

    @property
    def human_upload_date(self):
        """Ipload date format for human readers.."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")


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
        """Decorate saving with points assignments."""
        super(HomeworkSolutionComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
