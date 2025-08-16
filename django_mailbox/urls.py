from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SendMailAPIView, EmailConfigViewSet, index
)

app_name = 'django_mailbox'
router = DefaultRouter()

# 自动注册视图集路由

router.register(r'emailconfig', EmailConfigViewSet, basename='emailconfig')



urlpatterns = [
    path('send_mail/', SendMailAPIView.as_view()),
    path('email/', index, name='email'),
    path('', include(router.urls)),
]
