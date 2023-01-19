from django.shortcuts import render
from django.http import response
from django.core.files.storage import FileSystemStorage

##FOR SWAGGER
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi  
from rest_framework.parsers import MultiPartParser

from .util import OverwriteStorage, image_upload
from account.models import User, Follow
from .serializer import UserSerializer, SwaggerDeleteSerializer, FollowerSerializer, FolloweeSerializer, FollowSerializer



def index(req):
    return render(req, 'index.html')

# Create your views here.


class AccountView(APIView):
    parser_classes = [MultiPartParser]
    QueryUid = openapi.Parameter('uid', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="uid", default=2)
    
    @swagger_auto_schema(manual_parameters=[QueryUid] , operation_description='')
    def get(self, request):
        user = request.user
        key = request.GET.get('uid')
        if User.objects.filter(uid = key):
            user = User.objects.get(uid = key)
            serializer = UserSerializer(user)
            return response.JsonResponse(serializer.data, status=200)
        else:
            return response.JsonResponse({"status" : "user not found"})

    @swagger_auto_schema(request_body=UserSerializer, operation_description="ONLY ADD UID '7707'")
    def post(self, request):
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

    @swagger_auto_schema(request_body=UserSerializer, operation_description="ONLY USE UID 7707 , email not required(cannot be modified)")
    def put(self, request):
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

    @swagger_auto_schema(request_body=SwaggerDeleteSerializer, operation_description='ONLY USE UID 7707, SEND UID BY REQUEST_BODY')
    def delete(self, request):
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



class FollowView(APIView):
    follower = openapi.Parameter('follower', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="UID's follower", default=2)
    followee = openapi.Parameter('followee', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="UID's followee")

    @swagger_auto_schema(manual_parameters=[follower, followee])
    def get(self, request):
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

    @swagger_auto_schema(request_body=FollowSerializer)      
    def post(self, request):
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

    @swagger_auto_schema(request_body=FollowSerializer) 
    def delete(self, request):
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