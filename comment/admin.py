from django.contrib import admin
from .models import Comment
from tag_like.models import CommentTag

# Register your models here.

class CommentAdmin(admin.ModelAdmin):

    list_display = ('id', 'parent_id','post', 'author', 'content')


admin.site.register(Comment, CommentAdmin)