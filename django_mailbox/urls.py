from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SendMailAPIView, EmailConfigViewSet, index
)

from .views import batch_tasks_view,task_status


app_name = 'django_mailbox'
router = DefaultRouter()

# 自动注册视图集路由

router.register(r'emailconfig', EmailConfigViewSet, basename='emailconfig')



urlpatterns = [
    path('batch-tasks/', batch_tasks_view, name='batch_tasks'),
    path('task-status/', task_status, name='task_status'),

    path('send_mail/', SendMailAPIView.as_view()),
    path('email/', index, name='email'),
    path('', include(router.urls)),

    
]
