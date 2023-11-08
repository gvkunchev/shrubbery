from django.db import models
from django.utils import timezone
from django.apps import apps

from users.models import User
from points.models import PointsGiver

from .pygment import pygmentize


class Challenge(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    points = models.IntegerField(default=1)
    sanity_test = models.TextField()
    full_test = models.TextField(default="", null=True, blank=True)
    hidden = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    executing_tests = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        """String representation for the admin panel."""
        return self.title
    
    @property
    def can_upload(self):
        """Whether solutions can be uploaded or not."""
        if self.hidden:
            return False
        if self.verified:
            return False
        if self.deadline < timezone.now():
            return False
        return True

    @property
    def comments(self):
        """Get all comments."""
        return self.challengecomment_set.all()

    @property
    def human_deadline(self):
        """Deadline format for human readers.."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%d.%m.%Y %H:%M")

    @property
    def parsable_deadline(self):
        """Deadline that can be parsed by front-end."""
        return self.deadline.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%dT%H:%M")
    
    def save(self, *args, **kwargs):
        """Create action record for a new instance."""
        is_new = self.id is None
        super(Challenge, self).save(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.id}',
                                                                      date=self.creation_date,
                                                                      type='C')
            action.save()
    
    def get_pygmentized_sanity_test(self):
        return pygmentize(self.sanity_test)
    
    def get_pygmentized_full_test(self):
        return pygmentize(self.full_test)

class ChallengeComment(PointsGiver):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
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
        super(ChallengeComment, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Decorate saving with points assignments."""
        is_new = self.id is None
        super(ChallengeComment, self).save(*args, **kwargs)
        self._update_points(*args, **kwargs)
        if is_new:
            action = apps.get_model('activity.Action').objects.create(author=self.author,
                                                                      link=f'challenge/{self.challenge.id}#comment{self.id}',
                                                                      date=self.date,
                                                                      type='CC')
            action.save()

    def is_answered_by_teacher(self):
        """Is there an answer to the challenge from a teacher after this comment?"""
        for comment in self.challenge.comments:
            if comment.date > self.date:
                if comment.author.is_teacher():
                    return True
        return False


