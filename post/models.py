from django.db import models
from datetime import datetime
from account.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )
    title = models.TextField(
        null=True,
        blank=True,
        default=timezone.now

    )
    index = models.TextField(
        max_length=255,
        null=True
    )
    youtube_link = models.TextField(
        null=False
    )
    parent_id = models.IntegerField(
        null=True,
        blank=True
    )
    date = models.DateTimeField(
        default=datetime.now(),
        null=True,
    )

    def __str__(self):
        return self.title
