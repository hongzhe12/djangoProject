```bash
# 查看所有镜像
docker images

# 导出三个核心镜像（替换为你的实际镜像名）
docker save \
  djangoproject-web:latest \
  postgres:15-alpine \
  nginx:latest \
  > all_images.tar
```