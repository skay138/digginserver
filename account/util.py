import os
import requests
import uuid

from django.http import response
from django.core.files.storage import FileSystemStorage
from .serializer import UserSerializer
from django.conf import settings
from django.contrib.auth import login
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
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


@api_view(['GET',])
def google_callback(request):
    try:
        app_rest_api_key = settings.GOOGLE_API_KEY
        client_secret = settings.GOOGLE_CLIENT_KEY
        redirect_uri = '/'.join(['http://localhost:8000', "account/google/callback"])

        user_token = request.GET.get("code")

        # post request
        url = f"https://oauth2.googleapis.com/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}&client_secret={client_secret}"
        token_request = requests.post(url)
        token_response_json = token_request.json()
        error = token_response_json.get("error_description", None)
        
        # if there is an error from token_request
        if error is not None:
            return response.JsonResponse({"status":f"{error}"})
        access_token = token_response_json.get("access_token")
        
        # post request
        profile_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
            headers={"Authorization": "Bearer {}".format(access_token)},
        )
        profile_json = profile_request.json()

        # parsing profile json
        email = profile_json.get("email", None)
        if email is None:
            raise APIException()

        try:
            stage = "login"
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(
                uid = uuid.uuid4(),
                email=email,
                is_active=True
            )
            stage = "new"

        request.user = user
        return logged(request, stage) 

    except Exception as e:
        response.JsonResponse({"status" : "comeback strong"})