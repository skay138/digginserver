from django.urls import path
from . import views

urlpatterns = [
    path('<str:key>', views.comment_detail_view),
]