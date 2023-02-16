from django.shortcuts import render
from django.http import response
from .serializer import PostSerializer, PostSwaggerSerializer, PostDeleteSwaggerSerializer

##FOR SWAGGER
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()
from account.models import Follow
from .util import get_youtube_link

from django.utils import timezone
from datetime import timedelta

# Create your views here.

class PostView(APIView):
    number = openapi.Parameter('number', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, default=3)
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, default=1)

    @swagger_auto_schema(manual_parameters=[number, page],operation_description="")
    def get(self, request):

        number = int(request.GET.get('number', default=3))
        page = int(request.GET.get('page', default=1))
        post = Post.objects.latest('id')
        post_array = []
        collected_post = 0

        for i in range(post.id - (page-1)*number, 0, -1):
            if Post.objects.filter(id = i) and collected_post!= number:
                post_array.append(Post.objects.get(id = i))
                collected_post += 1
        serializer = PostSerializer(post_array, context={'author': request.user}, many=True)

        return response.JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(request_body=PostSwaggerSerializer)
    def post(self, request):
        data_user = request.data.get('uid')
        data_youtube_link = request.data.get('youtube_link')
        if User.objects.filter(uid=data_user):
            user = User.objects.get(uid=data_user)
            youtube_link, youtube_title, youtube_thumb = get_youtube_link(data_youtube_link)
            print(youtube_title)
            if youtube_link != None:
                post = Post.objects.create(
                    author = user,
                    youtube_link = youtube_link,
                    youtube_title = youtube_title,
                    youtube_thumb = youtube_thumb
                )
                for keys in request.data:
                    if hasattr(post, keys) == True:
                        if 'youtube_' in keys:
                            pass
                        else:
                            setattr(post, keys, request.data[keys])
                post.save()            
                return response.JsonResponse({"status": "good"})
            else:
                return response.JsonResponse({"status":"link error"}, status=400)
        else:
            return response.JsonResponse({"status": 'user not found'})



class PostDetailView(APIView):
    @swagger_auto_schema(tags=['PostDetail'])
    def get(self, request, post_id):
        if request.method == 'GET':
            if Post.objects.filter(id=post_id):
                post = Post.objects.get(id=post_id)
                serializer = PostSerializer(post, context={'author': request.user})
                return response.JsonResponse(serializer.data, status=200)
            else:
                return response.JsonResponse({"status" : "post not found"})

    @swagger_auto_schema(tags=['PostDetail'], request_body=PostSwaggerSerializer)
    def put(self, request, post_id):
        data_user = request.data.get('uid')
        data_youtube_link = request.data.get('youtube_link')
        varifyed_youtube_link, varifyed_youtube_title, varifyed_youtube_thumb = get_youtube_link(data_youtube_link)
        post = Post.objects.get(id=post_id)
        if varifyed_youtube_link == None:
            return response.JsonResponse({"status":"link error"}, status=400)
        if post.author.uid == data_user:
            for keys in request.data:
                if hasattr(post, keys) == True:
                    if keys == 'youtube_link':
                        post.youtube_link = varifyed_youtube_link
                    elif keys == 'youtube_title':
                        post.youtube_title = varifyed_youtube_title
                    elif keys == 'youtube_thumb':
                        post.youtube_thumb = varifyed_youtube_thumb
                    else:
                        setattr(post, keys, request.data[keys])
            post.save()
            return response.JsonResponse({"status": "good"})
        else:
            return response.JsonResponse({'status' : 'not author'})

    @swagger_auto_schema(tags=['PostDetail'], request_body=PostDeleteSwaggerSerializer)   
    def delete(self, request, post_id):
        data_author = request.data.get('uid')
        if Post.objects.filter(id = post_id):
            post = Post.objects.get(id=post_id)
            if (post.author.uid == data_author):
                post_title = post.title
                post.delete()
                return response.JsonResponse({"status" : f"{post_title} deleted"})
            else:
                return response.JsonResponse({"status" : "not author"})
        else:
            return response.JsonResponse({"status" : "post not found"})    
        

class PostSearchView(APIView):
    title = openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    author = openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    recommended = openapi.Parameter('recommended', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[title, author, recommended], operation_description="USE ONLY ONE PARAMETER")
    def get(self, request):
        if request.GET.get('title', default = None) != None :
            key = request.GET.get('title', default = None)
            post=Post.objects.filter(title__contains = key).order_by('-id')
            serializer = PostSerializer(post, context={'author': request.user}, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        elif request.GET.get('author', default = None) != None :
            key = request.GET.get('author', default = None)
            user = User.objects.filter(nickname__contains = key)
            post=Post.objects.filter(author__in = user).order_by('-id')
            serializer = PostSerializer(post, context={'author': request.user}, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        elif request.GET.get('recommended', default = None) != None :
            key = request.GET.get('recommended', default = None)
            one_week = timezone.now() - timedelta(weeks=1)
            post=Post.objects.filter(date__gt = one_week).order_by('-like_count','-id')[:int(key)]
            serializer = PostSerializer(post, context={'author': request.user}, many=True)
            return response.JsonResponse(serializer.data, safe=False)

        else:
            return response.JsonResponse({"status":"wrong request"})


class MyPostView(APIView):
    uid = openapi.Parameter('uid', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=2)
    @swagger_auto_schema(manual_parameters=[uid])
    def get(self, request):
        if request.GET.get('uid', default = None) != None :
            key = request.GET.get('uid')
            try : 
                author = User.objects.get(uid = key)
                post = Post.objects.filter(author = author).order_by('-id')
                serializer = PostSerializer(post, context={'author': request.user}, many=True)
                return response.JsonResponse(serializer.data, safe=False)
            except:
                return response.JsonResponse({"status":"user not found"})
        else :
            return response.JsonResponse({"status":"request error"})

class MyFeedView(APIView):
    uid = openapi.Parameter('uid', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=2)
    @swagger_auto_schema(manual_parameters=[uid])
    def get(self, request):
        if request.GET.get('uid', default = None) != None :
            key = request.GET.get('uid')
            try : 
                user = User.objects.get(uid = key)
            except:
                return response.JsonResponse({"status":"user not found"})
            follow = Follow.objects.filter(follower = user).values('followee')
            post = Post.objects.filter(author__in = follow).order_by('-id')
            serializer = PostSerializer(post, context={'author': request.user}, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        else :
            return response.JsonResponse({"status":"request error"})
