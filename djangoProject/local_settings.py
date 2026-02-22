INSTALLED_APPS = [
    "celery_demo.apps.CeleryDemoConfig",
    "django_mail",
]

# ==================== 跨域和 CSRF 配置 ====================
CSRF_TRUSTED_ORIGINS = [
    # 虚拟机IP
    "https://192.168.159.128",
]



# 本地开发
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"