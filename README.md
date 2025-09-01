```bash
# 查看所有镜像
docker images

# 导出三个核心镜像（替换为你的实际镜像名）
docker save \
  djangoproject-web:latest \
  postgres:15-alpine \
  nginx:latest \
  > all_images.tar

docker compose down && docker compose up --build -d
```
## 常用命令
```bash

# django服务常用
docker-compose exec web python manage.py check
docker-compose exec web pip install --no-index --find-links=python_packages -r requirements.txt
docker-compose exec web pip list | grep spark-ai-python
docker-compose exec web python -c "import sparkai; print('sparkai 导入成功')"
docker-compose restart web


# 验证任务注册情况
docker exec mysite-celery celery -A djangoProject inspect registered
docker exec mysite-celery celery -A djangoProject control inspect

# 在celery_worker中安装依赖
docker-compose exec celery_worker pip install --no-index --find-links=python_packages -r requirements.txt
docker-compose exec celery_worker pip list | grep spark-ai-python
docker-compose exec celery_worker python -c "import sparkai; print('sparkai 导入成功')"

# 在celery_beat中安装依赖
docker-compose exec celery_beat pip install --no-index --find-links=python_packages -r requirements.txt
docker-compose exec celery_beat pip list | grep spark-ai-python
docker-compose exec celery_beat python -c "import sparkai; print('sparkai 导入成功')"


# 重启生效注册任务生效
docker-compose restart
```