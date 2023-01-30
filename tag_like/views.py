from django.shortcuts import render
from django.http import response

##FOR SWAGGER
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema

#models
from post.models import Post
from .models import PostLike
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

# Create your views here.

class PostLikeSwaggerView(serializers.Serializer):
    uid = serializers.CharField(default = 2)
    post_id = serializers.IntegerField(default = 1)


class PostLikeView(APIView):

    @swagger_auto_schema(request_body=PostLikeSwaggerView)
    def post(self, request):
        data_uid = request.data.get('uid')
        data_post_id = request.data.get('post_id')
        try : 
            like_user = User.objects.get(uid = data_uid)
        except User.DoesNotExist:
            return response.JsonResponse({"status":'user does not exist'})
        
        try :
            like_post = Post.objects.get(id = data_post_id)
        except Post.DoesNotExist:
            return response.JsonResponse({"status":"post not exist"})
        
        if PostLike.objects.filter(user = like_user, post = like_post):
            return response.JsonResponse({"status":"already liked"})
        else:
            try :
                postlike = PostLike.objects.create(
                    user = like_user,
                    post = like_post
                )
                print(postlike)
                return response.JsonResponse({"status":"good"})
            except:
                return response.JsonResponse({"status":"error"})

    @swagger_auto_schema(request_body=PostLikeSwaggerView)
    def delete(self, request):
        data_uid = request.data.get('uid')
        data_post_id = request.data.get('post_id')
        try : 
            like_user = User.objects.get(uid = data_uid)
        except User.DoesNotExist:
            return response.JsonResponse({"status":'user does not exist'})
        
        try :
            like_post = Post.objects.get(id = data_post_id)
        except Post.DoesNotExist:
            return response.JsonResponse({"status":"post not exist"})
        
        if PostLike.objects.filter(user = like_user, post = like_post):
            postlike = PostLike.objects.get(user = like_user, post = like_post)
            postlike.delete()
            return response.JsonResponse({"status":"unliked"})
        else:
            print(PostLike.objects.filter(user = like_user, post = like_post))
            return response.JsonResponse({"status":"already unliked"})