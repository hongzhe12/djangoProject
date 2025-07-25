import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

# 实例化
app = Celery('djangoProject')

# namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从Django的已注册app中发现任务
app.autodiscover_tasks()