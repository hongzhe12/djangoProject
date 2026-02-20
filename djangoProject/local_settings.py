INSTALLED_APPS = [
    "mptt",
    "mdeditor",
    "django_mailbox",
    "article.apps.ArticleConfig",
    "users.apps.UsersConfig",
]

DEBUG = False  # 切换为生产环境

# ==================== 跨域和 CSRF 配置 ====================
CSRF_TRUSTED_ORIGINS = [
    # 虚拟机IP
    "https://192.168.159.128",
]
