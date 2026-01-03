#!/bin/sh

# 安装离线依赖(需要手动下载到 python_packages)
# pip install --no-index --find-links=/code/python_packages/ -r requirements.txt

# 安装在线依赖（子应用依赖）
find ./ -name requirements.txt ! -path "./requirements.txt" -exec pip install --trusted-host pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple -r {} \;

# 收集静态文件
python manage.py collectstatic --noinput

# 执行数据库迁移
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# 复制基座框架静态文件到指定位置
\cp -rf static/* /var/www/django_project/static/
# 复制子应用静态文件到指定位置
find ./ -type d -name static -exec sh -c 'rsync -av --ignore-existing "$1"/ /var/www/django_project/static/' _ {} \;

find ./ -type d -name media -exec sh -c 'rsync -av --ignore-existing "$1"/ /var/www/django_project/media/' _ {} \;

# 创建超级用户（如果不存在）
echo "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '1234')
    print('管理员用户已创建')
else:
    print('管理员用户已存在')
" | python manage.py shell

# /var/www/django_project/media/avatars/蓝色壁纸右边.png
# /var/www/django_project/media/avatars/%E8%93%9D%E8%89%B2%E5%A3%81%E7%BA%B8%E5%8F%B3%E8%BE%B9.png