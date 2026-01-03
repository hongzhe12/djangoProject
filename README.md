## 项目概述

这是一个基于Docker容器化的Django基座架，用于快速搭建Django项目。

## 环境准备

### 1. 证书生成（如需自签证书）

```bash
mkdir -p /etc/nginx/ssl/ && cd /etc/nginx/ssl/ && openssl req -x509 -newkey rsa:4096 -nodes -keyout server.key -out server.crt -days 365 -subj "/C=CN/ST=Zhejiang/L=Hangzhou/O=MyCompany/OU=IT/CN=localhost"
```


> **注意**：如使用正式域名，建议申请免费SSL证书，无需自签证书。

### 2. Nginx配置

将以下配置文件复制到Linux服务器对应目录：

- `etc/nginx/conf.d` 目录下的两个配置文件
- `etc/nginx/nginx.conf` 主配置文件

```bash
# 备份当前的nginx配置
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d_%H%M%S)
sudo cp -r /etc/nginx/conf.d/ /etc/nginx/conf.d.backup.$(date +%Y%m%d_%H%M%S)


# 替换主配置文件
sudo cp /root/djangoProject/etc/nginx/nginx.conf /etc/nginx/nginx.conf

# 替换conf.d目录下的文件
sudo cp /root/djangoProject/etc/nginx/conf.d/nginx.conf /etc/nginx/conf.d/
sudo cp /root/djangoProject/etc/nginx/conf.d/upstream_apps.conf /etc/nginx/conf.d/

# 检查nginx配置文件
sudo nginx -t

# 重启nginx
sudo service nginx restart

# 检查nginx运行状态
sudo service nginx status
```

### 3. 修改域名配置

编辑 `etc/nginx/conf.d/nginx.conf` 文件，修改 `server_name` 为：
- 有域名：使用您的正式域名
- 无域名：使用Nginx所在机器的IP地址

### 4. 添加跨域访问白名单
编辑`settings.py`的`CSRF_TRUSTED_ORIGINS`变量，添加你的域名，例如：https://admin.example.com

## 项目部署

### 启动服务

```bash
docker compose up -d
```


### 访问地址

项目启动成功后，可通过以下地址访问管理后台（账号admin，密码1234）：
```
# 管理后台
https://域名/o/app/admin/
# 例如
https://192.168.204.128/o/app/admin/
```
### 启动多套环境
```bash
# 切换另一个目录
mkdir -p /home/pre/djangoProject/ && cd /home/pre/djangoProject/
# 克隆项目
git clone https://github.com/hongzhe12/djangoProject.git


# 修改配置文件
1. 修改.env文件，修改访问路径前缀，修改为你自己需要的，例如 /t/baidu/ 
2. 修改.env文件，修改服务名称，例如 app2 必须唯一，否则会冲突服务无法启动
3. 修改.env文件，修改服务端口，例如 8081，必须唯一，否则会冲突服务无法启动

# 下面是一个例子

# .env
POSTGRES_USER=dev
POSTGRES_PASSWORD=password
POSTGRES_DB=dev
# docker配置
CONTAINER_NAME=app2
PORT=9000
# django配置
BASE_URL=/t/app/
STATIC_URL=/t/app/static/

# 启动服务（推荐指定名称）
docker-compose -p myapp_pre up -d
```



## 常用管理命令

### Django服务管理

```bash
# 检查Django项目配置
docker-compose exec web python manage.py check

# 安装项目依赖
docker-compose exec web pip install --no-index --find-links=python_packages -r requirements.txt

# 验证spark-ai-python包安装
docker-compose exec web pip list | grep spark-ai-python

# 测试sparkai模块导入
docker-compose exec web python -c "import sparkai; print('sparkai 导入成功')"

# 重启Django服务
docker-compose restart web
```


### Celery任务队列管理

#### 任务注册验证

```bash
# 查看已注册的Celery任务
docker exec mysite-celery celery -A djangoProject inspect registered

# 检查Celery状态
docker exec mysite-celery celery -A djangoProject control inspect
```


#### 依赖安装（Celery Worker）

```bash
# 安装依赖包
docker-compose exec celery_worker pip install --no-index --find-links=python_packages -r requirements.txt

# 验证spark-ai-python包
docker-compose exec celery_worker pip list | grep spark-ai-python

# 测试模块导入
docker-compose exec celery_worker python -c "import sparkai; print('sparkai 导入成功')"
```


#### 依赖安装（Celery Beat）

```bash
# 安装依赖包
docker-compose exec celery_beat pip install --no-index --find-links=python_packages -r requirements.txt

# 验证spark-ai-python包
docker-compose exec celery_beat pip list | grep spark-ai-python

# 测试模块导入
docker-compose exec celery_beat python -c "import sparkai; print('sparkai 导入成功')"
```


### 服务重启

```bash
# 重启所有服务以使新注册的任务生效
docker-compose restart
```


## 故障排查

- 如果无法访问管理后台，请检查Nginx配置和证书路径
- 如果Celery任务无法执行，请检查worker和beat容器状态
- 依赖包安装问题可参考Docker容器内的包管理命令

