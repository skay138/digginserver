from django.shortcuts import render
from django.http import response
from rest_framework.decorators import api_view

from .models import Comment
from post.models import Post
from account.models import User


from rest_framework import serializers

# Create your views here.
class CommentSerializer(serializers.ModelSerializer):
    def get_author_nickname(self, obj):
        return obj.author.nickname
    def get_author_uid(self, obj):
        return obj.author.uid

    nickname = serializers.SerializerMethodField('get_author_nickname')
    uid = serializers.SerializerMethodField('get_author_uid')

    class Meta:
        model = Comment
        fields = ['id', 'parent_id', 'uid', 'nickname', 'content',]

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def comment_detail_view(request, key):
    if request.method == 'GET':
        if Post.objects.filter(id=key):
            data_comment = Comment.objects.filter(post = key)
            serializer = CommentSerializer(data_comment, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        else:
            return response.JsonResponse({"status":"post not found"})

    elif request.method == 'POST':
        if Post.objects.filter(id=key): 
            if User.objects.filter(uid=request.data.get('uid')):
                data_uid = request.data.get('uid')
                data_post = Post.objects.get(id=key)
                user = User.objects.get(uid=data_uid)
                comment = Comment.objects.create(
                    author = user,
                    post = data_post
                )
                for keys in request.data:
                    if hasattr(comment, keys) == True:
                        setattr(comment, keys, request.data[keys])
                comment.save()
                return response.JsonResponse({"status":"good"})
            else:
                return response.JsonResponse({"status":"user not found"})
        else:
            return response.JsonResponse({"status":"post not found"})
    
    elif request.method == 'PUT':
        if Comment.objects.filter(id=key):
            pass
        else:
            return response.JsonResponse({"status":"comment not found"})
        data_uid = request.data.get('uid')
        comment = Comment.objects.get(id = key)
        if comment.author.uid == data_uid :
            for keys in request.data:
                if hasattr(comment, keys) == True:
                    setattr(comment, keys, request.data[keys])
            comment.save()
            return response.JsonResponse({"status":"good"})
        else:
            return response.JsonResponse({"status":"not author"})

    elif request.mothod == 'DELETE':
        if Comment.objects.filter(id=key):
            pass
        else:
            return response.JsonResponse({"status":"comment not found"})

        data_uid = request.data.get('uid')
        comment = Comment.objects.get(id = key)
        if comment.author.uid == data_uid :
            comment_content = comment.content
            comment.delete()
            return response.JsonResponse({"status":f"{comment_content} deleted"})
        else:
            return response.JsonResponse({"status":"not author"})