from django.shortcuts import render
from django.http import response
from rest_framework.decorators import api_view

from .models import Post
from account.models import User
from rest_framework import serializers
from .util import get_youtube_info, youtube_link_varify

# Create your views here.
class PostSerializer(serializers.ModelSerializer):
    def get_author_nickname(self, obj):
        return obj.author.nickname
    def get_author_uid(self, obj):
        return obj.author.uid
    def get_video_data(self, obj):
        return get_youtube_info(obj.youtube_link)
    
    nickname = serializers.SerializerMethodField('get_author_nickname')
    uid = serializers.SerializerMethodField('get_author_uid')
    youtube_data = serializers.SerializerMethodField('get_video_data')

    class Meta :
        model = Post
        fields = ['id', 'parent_id','title', 'content', 'youtube_link', 'nickname', 'uid', 'date', 'youtube_data']

@api_view(['POST', 'GET'])
def post_view(request):
    if request.method == 'GET':
        number = int(request.GET.get('number', default=3))
        page = int(request.GET.get('page', default=1))
        post = Post.objects.latest('id')
        post_array = []
        collected_post = 0

        for i in range(post.id - (page-1)*number, 0, -1):
            if Post.objects.filter(id = i) and collected_post!= number:
                post_array.append(Post.objects.get(id = i))
                collected_post += 1
        serializer = PostSerializer(post_array, many=True)

        return response.JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data_user = request.data.get('uid')
        data_youtube_link = request.data.get('youtube_link')
        if youtube_link_varify(data_youtube_link):
            pass
        else :
            return response.JsonResponse({"status":"youtube_link_error"})
        if User.objects.filter(uid=data_user):
            user = User.objects.get(uid=data_user)
            post = Post.objects.create(
                author = user,
                youtube_link = data_youtube_link
            )
            for keys in request.data:
                if hasattr(post, keys) == True:
                    setattr(post, keys, request.data[keys])
            post.save()            
            return response.JsonResponse({"status": "good"})
        else:
            return response.JsonResponse({"status": 'user not found'})

@api_view(['PUT', 'GET', 'DELETE'])
def post_detail_view(request, pk):
    if request.method == 'GET':
        if Post.objects.filter(id=pk):
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post)
            return response.JsonResponse(serializer.data, status=200)
        else:
            return response.JsonResponse({"status" : "post not found"})
    
    elif request.method == 'PUT':
        data_user = request.data.get('uid')
        youtube_link = request.data.get('youtube_link')
        post = Post.objects.get(id=pk)
        if youtube_link_varify(youtube_link):
            pass
        else :
            return response.JsonResponse({"status":"youtube_link_error"})
        if post.author.uid == data_user:
            for keys in request.data:
                if hasattr(post, keys) == True:
                    setattr(post, keys, request.data[keys])
            post.save()
            return response.JsonResponse({"status": "good"})
        else:
            return response.JsonResponse({'status' : 'not author'})

    elif request.method == 'DELETE':
        data_author = request.data.get('uid')
        if Post.objects.filter(id = pk):
            post = Post.objects.get(id=pk)
            if (post.author.uid == data_author):
                post_title = post.title
                post.delete()
                return response.JsonResponse({"status" : f"{post_title} deleted"})
            else:
                return response.JsonResponse({"status" : "not author"})
        else:
            return response.JsonResponse({"status" : "post not found"})



@api_view(['GET'])
def posts_search_view(request):
    if request.method == 'GET':
        if request.GET.get('title', default = None) != None :
            key = request.GET.get('title', default = None)
            post=Post.objects.filter(title__contains = key).order_by('-id')
            serializer = PostSerializer(post, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        elif request.GET.get('author', default = None) != None :
            key = request.GET.get('author', default = None)
            user = User.objects.filter(nickname__contains = key)
            post=Post.objects.filter(author__in = user).order_by('-id')
            serializer = PostSerializer(post, many=True)
            return response.JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def my_posts_view(request):
    if request.GET.get('uid', default = None) != None :
        key = request.GET.get('uid')
        author = User.objects.get(uid = key)
        post = Post.objects.filter(author = author).order_by('-id')
        serializer = PostSerializer(post, many=True)
        return response.JsonResponse(serializer.data, safe=False)
    else :
        return response.JsonResponse({"status":"request error"})
    