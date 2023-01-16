from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_view),
    path('<int:pk>', views.post_detail_view),
    path('mypost', views.my_posts_view),
    path('search', views.posts_search_view)
]