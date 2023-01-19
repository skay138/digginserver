from django.urls import path
from . import views

urlpatterns = [
    path('<str:key>', views.CommentView.as_view()),
]