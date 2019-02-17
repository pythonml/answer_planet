from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ("Easy", "简单"),
        ("Medium", "中等"),
        ("Hard", "困难"),
    )
    question_text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)
    count_down = models.IntegerField(default=10)
    score = models.IntegerField()

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=1)
    option_text = models.TextField()
    is_correct = models.BooleanField()

class User(AbstractUser):
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True)
    invited_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    invite_code = models.CharField(max_length=10, unique=True)
    daily_limit = models.IntegerField(default=0)

class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Option, on_delete=models.CASCADE)

class UserEvent(models.Model):
    EVENT_CHOICES = (
        ("answer", "answer"),
        ("invite", "invite_bonus")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    event_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    user_answer = models.ForeignKey(UserAnswer, null=True, on_delete=models.CASCADE)

class UserTotalScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    total_score = models.IntegerField(default=0)
