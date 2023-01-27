from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Post
from .util import get_youtube_info


class PostSerializer(serializers.ModelSerializer):
    def get_author_nickname(self, obj):
        return obj.author.nickname
    def get_author_uid(self, obj):
        return obj.author.uid
    def get_video_data(self, obj):
        return get_youtube_info(obj.youtube_link)

    def get_parent_author(self, obj):
        if obj.parent_id:
            post_parent_id = obj.parent_id
            post = Post.objects.get(id = post_parent_id)
            parent_author = {
                'id' : post_parent_id,
                'uid' : post.author.uid,
                'nickname' : post.author.nickname,
                'image' : post.author.image.url
            }
            return parent_author
        else:
            return    

    nickname = serializers.SerializerMethodField('get_author_nickname')
    uid = serializers.SerializerMethodField('get_author_uid')
    youtube_data = serializers.SerializerMethodField('get_video_data')
    parent = serializers.SerializerMethodField('get_parent_author')

    class Meta :
        model = Post
        fields = ['id','parent','title', 'content', 'youtube_link', 'nickname', 'uid', 'date', 'youtube_data']

class PostSwaggerSerializer(serializers.Serializer):
    uid= serializers.CharField(help_text='작성자 uid', default=7707)
    title = serializers.CharField(help_text='타이틀')
    content = serializers.CharField(help_text='글 내용')
    youtube_link = serializers.CharField(help_text = 'youtube 링크')
    parent_id = serializers.IntegerField(help_text='리포스트의 포스트id')

class PostDeleteSwaggerSerializer(serializers.Serializer):
    uid= serializers.CharField(help_text='작성자 uid', default=7707)