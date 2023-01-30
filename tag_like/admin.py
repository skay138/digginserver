from django.contrib import admin
from .models import PostLike, CommentTag

# Register your models here.

class PostLikeAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'post')

class TagUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'comment')


admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentTag, TagUserAdmin)