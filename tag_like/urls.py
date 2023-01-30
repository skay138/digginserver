from django.urls import path
from . import views

urlpatterns = [
    path('postlike', views.PostLikeView.as_view())
]