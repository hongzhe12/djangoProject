from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SendMailAPIView, EmailConfigViewSet, index
)

from .views import batch_tasks_view,task_status,export_tasks_excel,export_tasks_summary_excel


app_name = 'django_mailbox'
router = DefaultRouter()

# 自动注册视图集路由

router.register(r'emailconfig', EmailConfigViewSet, basename='emailconfig')



urlpatterns = [
    path('batch-tasks/', batch_tasks_view, name='batch_tasks'),
    path('task-status/', task_status, name='task_status'),  # 不带参数的路由（用于默认显示最新）
    path('task-status/<uuid:batch_id>/', task_status, name='task_status'),

    path('task-status/<uuid:batch_id>/export/', export_tasks_excel, name='export_tasks_excel'),
    path('task-status/<uuid:batch_id>/export-summary/', export_tasks_summary_excel, name='export_summary_excel'),


    path('send_mail/', SendMailAPIView.as_view()),
    path('email/', index, name='email'),
    path('', include(router.urls)),
]
