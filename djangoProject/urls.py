"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from djangoProject.settings import BASE_URL

try:
    from rest_framework_simplejwt.views import TokenObtainPairView
except ImportError:
    TokenObtainPairView = None


def prefixed_path(route, view, base_url=BASE_URL, name=None):
    """自动添加base_url前缀的辅助函数"""
    base_url_stripped = base_url.strip("/")
    full_route = f"{base_url_stripped}/{route}" if base_url_stripped else route
    return path(full_route, view, name=name)

# 基础框架，勿动
urlpatterns = [
    prefixed_path("admin/", admin.site.urls),
]

if TokenObtainPairView is not None:
    urlpatterns.append(
        prefixed_path('api/token/', TokenObtainPairView.as_view(), name='token_obtain')
    )

# 自定义url
urlpatterns += [
    prefixed_path("django_mail/", include("django_mail.urls")),
    prefixed_path("celery-demo/", include("celery_demo.urls")),
    prefixed_path("api/", include("todo.urls")),
]
