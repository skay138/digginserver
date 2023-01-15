from django.contrib import admin
from .models import Post

# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'index', 'author', 'youtube_link')


admin.site.register(Post, PostsAdmin)