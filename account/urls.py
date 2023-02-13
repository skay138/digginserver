from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.AccountView.as_view()),
    path('search', views.AccountSearchView.as_view()),
    path('follow', views.FollowView.as_view()),
    path('firebaselogin', views.FirebaseLoginView.as_view())
]

