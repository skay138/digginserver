from django.contrib import admin
from .models import Post
from comment.models import Comment
from rest_framework import serializers
# Register your models here.



class PostsAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'content', 'author', 'youtube_link', 'like_count')
    list_display_links=('title',)


admin.site.register(Post, PostsAdmin)