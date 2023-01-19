from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from .util import google_callback

urlpatterns = [
    path('', views.AccountView.as_view()),
    path('follow', views.FollowView.as_view()),
    path('google/callback', google_callback)
]

