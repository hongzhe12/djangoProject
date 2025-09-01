from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SendMailAPIView, EmailConfigViewSet, index
)

from .views import start_sparkai_chat,check_sparkai_result

app_name = 'django_mailbox'
router = DefaultRouter()

# 自动注册视图集路由

router.register(r'emailconfig', EmailConfigViewSet, basename='emailconfig')



urlpatterns = [
    path('api/chat/start/', start_sparkai_chat, name='start_chat'),
    path('api/chat/result/<str:task_id>/', check_sparkai_result, name='check_result'),
    path('send_mail/', SendMailAPIView.as_view()),
    path('email/', index, name='email'),
    path('', include(router.urls)),
]
