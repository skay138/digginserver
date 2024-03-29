"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings  # new
from django.conf.urls.static import static  # new
import config.views
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi

schema_url_patterns = [
    path('', include('config.urls'))
]
schema_view_v1 = get_schema_view(
    openapi.Info(
        title="DIGGIN BACKEND APIS",
        default_version='v1',
        description="THIS IS DIGGIN BACKEND API TEST PAGE\n\nBasic authorization>> CLICK Authorize Button on the right \n username : test@test.com \n password : 1",
        #terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    path('', config.views.index, name='index'),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('account/', include('account.urls')),
    path('comment/', include('comment.urls')),
    path('taglike/', include('tag_like.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]


if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)