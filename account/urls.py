from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view),
    path('<str:key>', views.account_detail_view)
    # path('<int:pk>', views.post_detail_view),
    # path('get/<int:key>/<int:page>', views.get_posts_view),
    # path('mypost/<str:key>', views.my_posts_view)
    # path('/search/<int:pk>',views.search_view),
    # path('/title/<text:title>',views.title_view)
]