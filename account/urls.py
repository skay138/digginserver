from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view),
    path('follow', views.follow_view)
]