from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    word = models.CharField(max_length=256, null=False)
    meaning = models.TextField(null=False)
    example = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Mark(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    CHOICES = {
        LIKE: 'like',
        DISLIKE: 'dislike',
    }
    mark = models.CharField(max_length=7, choices=CHOICES)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
