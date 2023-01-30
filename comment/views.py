from django.shortcuts import render
from django.http import response

##FOR SWAGGER
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

from .models import Comment
from post.models import Post
from tag_like.models import CommentTag
from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers

# Create your views here.

class CommentSerializer(serializers.ModelSerializer):
    def get_author_nickname(self, obj):
        return obj.author.nickname
    def get_author_uid(self, obj):
        return obj.author.uid
    def get_author_image(self, obj):
        return obj.author.image.url

    def get_tag_user(self, obj):
        class TagUserSerializer(serializers.ModelSerializer):

            class Meta:
                model = CommentTag
                fields = ['user']

        tag_user_list = []

        if CommentTag.objects.filter(comment=obj.id):
            tag_user = CommentTag.objects.filter(comment=obj.id)
            tag_user_serializer = TagUserSerializer(tag_user, many=True).data
            for keys in tag_user_serializer:
                tag_user_list.append(keys['user'])
            return tag_user_list
        else :
            return None


    nickname = serializers.SerializerMethodField('get_author_nickname')
    uid = serializers.SerializerMethodField('get_author_uid')
    image = serializers.SerializerMethodField('get_author_image')
    taguser = serializers.SerializerMethodField('get_tag_user')

    class Meta:
        model = Comment
        fields = ['id', 'parent_id', 'uid', 'nickname', 'image', 'content', 'taguser']
    
class SwaggerCommentSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(default = 7707)
    tag_uid = serializers.ListField()

    
    class Meta:
        model = Comment
        fields = ['uid', 'content', 'tag_uid', 'parent_id']

class SwaggerCommentDeleteSerializer(serializers.ModelSerializer):
    uid = serializers.CharField()

    class Meta:
        model = Comment
        fields = ['uid']
    


class CommentView(APIView):

    @swagger_auto_schema(operation_description="KEY IS POST_ID")
    def get(self, request, key):
        if Post.objects.filter(id=key):
            data_comment = Comment.objects.filter(post = key)
            serializer = CommentSerializer(data_comment, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        else:
            return response.JsonResponse({"status":"post not found"})
        
    @swagger_auto_schema(request_body=SwaggerCommentSerializer, operation_description="KEY IS POST_ID")
    def post(self, request, key):
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
                if request.data.get('tag_uid'):
                    for users in request.data.get('tag_uid'):
                        try : 
                            tag_user = User.objects.get(uid = users)
                            CommentTag.objects.create(
                                user = tag_user,
                                comment = comment
                            )
                        except:
                            pass
                return response.JsonResponse({"status":"good"})
            else:
                return response.JsonResponse({"status":"user not found"})
        else:
            return response.JsonResponse({"status":"post not found"})

    @swagger_auto_schema(request_body=SwaggerCommentSerializer, operation_description="KEY IS POST_ID")
    def put(self, request, key):
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
            if request.data.get('tag_uid'):
                for users in request.data.get('tag_uid'):
                    try : 
                        tag_user = User.objects.get(uid = users)
                        CommentTag.objects.create(
                            user = tag_user,
                            comment = comment
                        )
                    except:
                        pass
            return response.JsonResponse({"status":"good"})
        else:
            return response.JsonResponse({"status":"not author"})
    
    @swagger_auto_schema(request_body=SwaggerCommentDeleteSerializer, operation_description="KEY IS COMMENT_ID")
    def delete(self, request, key):
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