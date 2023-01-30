from django.db import models
from account.models import User
from post.models import Post

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment_post_id'
    )
    content = models.TextField(
        null=True,
        blank=True,
    )
    parent_id = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        if self.content:
            return self.content
        else :
            return 'no content'