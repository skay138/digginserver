from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_view),
    path('<int:pk>', views.post_detail_view),
    path('<int:key>/<int:page>', views.get_posts_view),
    path('search/<str:key>', views.posts_search_view),
    path('mypost/<str:key>', views.my_posts_view)
]