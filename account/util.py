import os
import requests

from django.http import response
from django.core.files.storage import FileSystemStorage
from .serializer import UserSerializer
from django.conf import settings
from django.contrib.auth import login
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model

User = get_user_model()



class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def image_upload(uid):
    path = 'profile_image/'
    return f'{path}{uid}.png'

def logged(request, stage):
    login(request, request.user)

    user = request.user
    print(user)
    serializer = UserSerializer(user)
    if stage == 'new':
        return response.JsonResponse(serializer.data, status=201)
    elif stage == 'login':
        return response.JsonResponse(serializer.data, status=200)