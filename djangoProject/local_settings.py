
INSTALLED_APPS = [
    "django_mailbox",
    "article.apps.ArticleConfig",
    "users.apps.UsersConfig",
]

DEBUG = False  # 切换为生产环境

# ==================== 跨域和 CSRF 配置 ====================
CSRF_TRUSTED_ORIGINS = ["http://192.168.204.128:80", "https://192.168.204.128"]
