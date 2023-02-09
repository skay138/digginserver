from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view()),
    path('<int:post_id>', views.PostDetailView.as_view()),
    path('mypost', views.MyPostView.as_view()),
    path('myfeed', views.MyFeedView.as_view()),
    path('search', views.PostSearchView.as_view())
]