from django.shortcuts import render
from django.http import response
from rest_framework.decorators import api_view
from datetime import datetime

from account.models import User
from rest_framework import serializers

# Create your views here.
class UserSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ['nickname','introduce','image','is_active']

@api_view(['POST', 'GET'])
def account_view(request):
    if request.method == 'GET':
        return response.JsonResponse({"status" : "not build"})

    elif request.method == 'POST':
        data_uid = request.data.get('uid')
        data_email = request.data.get('email')
        data_nickname = request.data.get('nickname')
        data_gender = request.data.get('gender')
        data_birth = request.data.get('birth')
        data_introduce = request.data.get('introduce')
        data_image = request.data.get('image')

        if User.objects.filter(uid = data_uid):
            return response.JsonResponse({"status" : "already exist"})
        else:
            try:
                User.objects.create(
                    uid = data_uid,
                    email = data_email,
                    nickname = data_nickname,
                    gender = data_gender,
                    birth = data_birth,
                    introduce = data_introduce,
                    image = data_image,
                    date_joined = datetime.now()
                )
                return response.JsonResponse({"status" : "good"})
            except:
                return response.JsonResponse({"status": "error"})


@api_view(['GET', 'DELETE', 'PUT'])
def account_detail_view(request, key):
    if request.method == 'GET':
        if User.objects.filter(uid = key):
            user = User.objects.get(uid = key)
            serializer = UserSerializer(user)
            return response.JsonResponse(serializer.data, status=200)
        else:
            return response.JsonResponse({"status" : "user not found"})

    elif request.method == 'PUT':
        if User.objects.filter(uid = key): 
            user = User.objects.get(uid = key)
            for keys in request.data:
                if hasattr(user, keys) == True:
                    setattr(user, keys, request.data[keys])
            user.save()
            return response.JsonResponse({"status": "good"})
        else:
            return response.JsonResponse({"status" : "user not found"})
    elif request.method == 'DELETE':
        if User.objects.filter(uid = key):
            user = User.objects.get(uid = key)
            user.delete()
            return response.JsonResponse({"status" : "good"})
        else:
            return response.JsonResponse({"status" : "user not found"})
