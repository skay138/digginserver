from django.db import models
from account.models import User
from post.models import Post
from comment.models import Comment

# Create your models here.

class PostLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='like_user'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='like_post'
    )