from django.urls import path

from .views import EnqueueAddView, EnqueueEchoView, TaskStatusView

app_name = "celery_demo"

urlpatterns = [
    path("add/", EnqueueAddView.as_view(), name="enqueue_add"),
    path("echo/", EnqueueEchoView.as_view(), name="enqueue_echo"),
    path("status/<str:task_id>/", TaskStatusView.as_view(), name="task_status"),
]
