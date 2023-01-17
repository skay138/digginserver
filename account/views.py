from django.shortcuts import render
from django.http import response
from rest_framework.decorators import api_view

from django.core.files.storage import FileSystemStorage
from .util import OverwriteStorage, image_upload

from account.models import User, Follow
from rest_framework import serializers


def index(req):
    return render(req, 'index.html')

# Create your views here.
class UserSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ['uid','nickname','introduce','image','is_active']

class FollowerSerializer(serializers.ModelSerializer):
    def get_nickname(self, obj):
        return obj.follower.nickname

    def get_image(self, obj):
        return obj.follower.image
    
    nickname = serializers.SerializerMethodField('get_nickname')
    image = serializers.SerializerMethodField('get_image')

    class Meta :
        model = Follow
        fields = ['follower', 'nickname', 'image']

class FolloweeSerializer(serializers.ModelSerializer):
    def get_nickname(self, obj):
        return obj.followee.nickname

    def get_image(self, obj):
        return obj.followee.image

    nickname = serializers.SerializerMethodField('get_nickname')
    image = serializers.SerializerMethodField('get_image')

    class Meta :
        model = Follow
        fields = ['followee', 'nickname', 'image']

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def account_view(request):
    if request.method == 'GET' :
        key = request.GET.get('uid')
        if User.objects.filter(uid = key):
            user = User.objects.get(uid = key)
            serializer = UserSerializer(user)
            return response.JsonResponse(serializer.data, status=200)
        else:
            return response.JsonResponse({"status" : "user not found"})
               
    elif request.method == 'POST':
        if request.data.get('uid'):
            data_uid = request.data.get('uid')
            print(data_uid)
        else:
            return response.JsonResponse({"status":"uid or path error"})
        data_email = request.data.get('email')
        data_nickname = request.data.get('nickname')
        if User.objects.filter(uid = data_uid) or User.objects.filter(email = data_email):
            return response.JsonResponse({"status" : "already exist"})
        else:
                user = User.objects.create(
                    uid = data_uid,
                    email = data_email,
                    nickname = data_nickname)
                for keys in request.data:
                    if hasattr(user, keys) == True:
                        if keys == 'image' and request.FILES.get('image'):
                            data_image = request.FILES.get('image')
                            setattr(user, keys, FileSystemStorage().save(image_upload(user.uid), data_image))
                        else:
                            setattr(user, keys, request.data[keys])
                user.save()
                return response.JsonResponse({"status" : "good"}, status=201)
    elif request.method == 'PUT':
        if request.data.get('uid'):
            data_uid = request.data.get('uid')
            print(data_uid)
        else:
            return response.JsonResponse({"status":"uid error"})
        if User.objects.filter(uid = data_uid): 
            user = User.objects.get(uid = data_uid)
            for keys in request.data:
                if hasattr(user, keys) == True:
                    if keys == 'image' and request.FILES.get('image'):
                        data_image = request.FILES.get('image')
                        setattr(user, keys, OverwriteStorage().save(image_upload(user.uid), data_image))
                    elif keys == 'uid' or keys == 'email':
                        pass
                    else:
                        setattr(user, keys, request.data[keys])
            user.save()
            return response.JsonResponse({"status": "good"})
        else:
            return response.JsonResponse({"status" : "user not found"})      

    elif request.method == 'DELETE':
        if request.data.get('uid'):
            data_uid = request.data.get('uid')
            print(data_uid)
        else:
            return response.JsonResponse({"status":"uid error"})
        if User.objects.filter(uid = data_uid):
            user = User.objects.get(uid = data_uid)
            image = str(user.image)
            FileSystemStorage().delete(image)
            user.delete()
            return response.JsonResponse({"status" : "good"})
        else:
            return response.JsonResponse({"status" : "user not found"})



@api_view(['GET', 'POST', 'DELETE'])
def follow_view(request):
    if request.method == 'GET':
        if request.GET.get('follower', default = None) != None:
            key = request.GET.get('follower', default = None)
            follower = Follow.objects.filter(followee = key)
            serializer = FollowerSerializer(follower, many=True)
            return response.JsonResponse(serializer.data, safe=False)
            
        elif request.GET.get('followee', default = None) != None:
            key = request.GET.get('followee', default = None)
            followee = Follow.objects.filter(follower = key)
            serializer = FolloweeSerializer(followee, many=True)
            print(serializer.data)
            return response.JsonResponse(serializer.data, safe=False)
        else:
            return response.JsonResponse({"status": "bad request"})
    if request.method == 'POST':
        try : 
            data_follower = User.objects.get(uid = request.data.get('follower'))
            data_followee = User.objects.get(uid = request.data.get('followee'))
        except :
            return response.JsonResponse({"status" : "follow user not found"})

        if Follow.objects.filter(follower = data_follower, followee=data_followee):
            return response.JsonResponse({"status":"already following"})
        else:
            Follow.objects.create(
                follower = data_follower,
                followee = data_followee
            )
            return response.JsonResponse({"status":"done"})
    elif request.method == 'DELETE':
        try : 
            data_follower = User.objects.get(uid = request.data.get('follower'))
            data_followee = User.objects.get(uid = request.data.get('followee'))
        except :
            return response.JsonResponse({"status" : "follow user not found"})

        if Follow.objects.filter(follower = data_follower, followee=data_followee):
            Follow.objects.get(follower = data_follower, followee=data_followee).delete()
            return response.JsonResponse({"status":"unfollow done"})
        else:
            return response.JsonResponse({"status" : "already unfollowed"})
