#!/bin/sh

# 安装离线依赖(需要手动下载到 python_packages)
# pip install --no-index --find-links=/code/python_packages/ -r requirements.txt


# 执行数据库迁移
python manage.py migrate --noinput

# 复制静态文件到指定位置
\cp -rf static/* /var/www/django_project/static/

# 收集静态文件
python manage.py collectstatic --noinput

# 创建超级用户（如果不存在）
echo "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '1234')
    print('管理员用户已创建')
else:
    print('管理员用户已存在')
" | python manage.py shell

# 启动 Django 开发服务器
exec uvicorn djangoProject.asgi:application --host 0.0.0.0 --port 8000 --workers 10