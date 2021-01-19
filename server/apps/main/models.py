from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField

MAX_QUESTION_VARIANTS = 10


class Question(models.Model):
    """ Model representing the pool"""

    types = (
        ("ONE", "One correct"),
        ("MULTIPLE", "Multiple correct"),
        ("TEXT", "Text answer"),
    )
    description = models.TextField()

    type = models.CharField(max_length=100, choices=types)
    variants = ArrayField(
        models.CharField(max_length=100, blank=True),
        size=MAX_QUESTION_VARIANTS,
    )
    answers = ArrayField(
        ArrayField(
            models.CharField(max_length=100, blank=True), size=MAX_QUESTION_VARIANTS
        )
    )


# Create your models here.
class Poll(models.Model):
    """ Model representing the pool """

    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    questions = models.ManyToManyField(Question, related_name="questions")
    description = models.TextField()

    @staticmethod
    def get_active():
        return Poll.objects.filter(
            start_date__gte=datetime.now(), end_date__lte=datetime.now()
        )

    @property
    def is_active(self):
        return self.start_date >= datetime.now() and self.end_date <= datetime.now()


class PassedPoll(models.Model):
    """ Model representing poll passed by the user """

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answers = ArrayField(ArrayField(models.CharField(max_length=100, blank=True)))

    @property
    def valid(self):
        return True


class History(models.Model):
    """ Model representing all polls passed by the user """

    user_id = models.IntegerField()
    passes = models.ManyToManyField(PassedPoll)
