from django.contrib import admin
from django.urls import path, include
from djangoProject.settings import BASE_URL


def prefixed_path(route, view, base_url=BASE_URL, name=None):
    """自动添加base_url前缀的辅助函数"""
    base_url_stripped = base_url.strip("/")
    full_route = f"{base_url_stripped}/{route}" if base_url_stripped else route
    return path(full_route, view, name=name)

urlpatterns = [
    prefixed_path("article/", include("article.urls")),
    prefixed_path("users/", include("users.urls")),
]
