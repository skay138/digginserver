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
from drf_yasg             import openapi 
from rest_framework import serializers

# Create your views here.

class PostLikeSwaggerView(serializers.Serializer):
    uid = serializers.CharField(default = 2)
    post_id = serializers.IntegerField(default = 1)


class PostLikeView(APIView):
    post_id = openapi.Parameter('post_id', openapi.IN_QUERY, type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(manual_parameters=[post_id])
    def get(self, request):
        user_header = request.META.get('HTTP_AUTHORIZATION')
        try :
            current_user = User.objects.get(uid = user_header)
        except:
            current_user = request.user
        post_id = request.GET.get('post_id')
        try :
            post = Post.objects.get(id = post_id)
            like_count = PostLike.objects.filter(post = post).count()
        except:
            return response.JsonResponse({'status':'post not found'}, status = 300)

        try : 
            PostLike.objects.get(user = current_user, post = post)
            return response.JsonResponse({"status":True, "count": like_count}, status = 200)
        except:
            return response.JsonResponse({"status":False, "count":like_count}, status = 201)


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
                PostLike.objects.create(
                    user = like_user,
                    post = like_post
                )
                post = Post.objects.get(id = data_post_id)
                post.like_count = PostLike.objects.filter(post = data_post_id).count()
                post.save()
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
            post = Post.objects.get(id = data_post_id)
            post.like_count = PostLike.objects.filter(post = data_post_id).count()
            post.save()
            return response.JsonResponse({"status":"unliked"})
        else:
            print(PostLike.objects.filter(user = like_user, post = like_post))
            return response.JsonResponse({"status":"already unliked"})