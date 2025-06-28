from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmailConfigViewSet, index
)


router = DefaultRouter()

# 自动注册视图集路由

router.register(r'emailconfig', EmailConfigViewSet, basename='emailconfig')


urlpatterns = [
    path('', index, name='email_config'),
    path('api/', include(router.urls)),

    # 在此添加其他自定义路由
]