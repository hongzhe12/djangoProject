# your_app/admin.py

from django.contrib import admin
from .models import EmailConfig

# 注册 EmailConfig 模型到后台管理
admin.site.register(EmailConfig)