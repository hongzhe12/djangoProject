# Django 基座项目

这是一个基于 Django + DRF + Celery + Docker 的项目基座，当前已包含：

- Django 管理后台
- 邮件配置与发送模块 `django_mail`
- Celery Demo

## 项目结构

- `djangoProject/`：项目配置、路由、Celery 配置
- `django_mail/`：邮件相关应用
- `celery_demo/`：Celery 示例应用
- `etc/nginx/`：Nginx 配置
- `static/`：静态资源

## 运行环境

推荐使用 `uv` 管理 Python 依赖。

安装依赖（包含子应用）、拷贝迁移静态资源：

```bash
./init.sh
```

如果只想补齐单个依赖：

```bash
uv add django-extensions
```

## 本地启动

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

后台地址默认：

- http://127.0.0.1:8000/o/app/admin/

## 接口鉴权说明

当前项目的鉴权是基于 JWT 的，配置位置如下：

- [djangoProject/settings.py](djangoProject/settings.py)：
  - `REST_FRAMEWORK` 中启用了 `JWTAuthentication`
  - 如果未安装 `djangorestframework-simplejwt`，项目会自动降级，不会因为导入失败而启动报错
- [djangoProject/urls.py](djangoProject/urls.py)：
  - 暴露了登录签发令牌接口 `api/token/`

### 当前实际效果

需要注意：

- 目前项目只配置了“认证方式”，没有强制所有接口都必须登录
- 如果请求里带上 JWT，DRF 会识别为已登录用户

### 获取 Token

先使用用户名和密码换取 JWT：

```bash
curl -X POST http://127.0.0.1:8000/o/app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"1234"}'
```

返回示例：

```json
{
  "refresh": "xxx",
  "access": "yyy"
}
```

### `require_jwt` 装饰器

项目里提供了一个简单的 JWT 鉴权装饰器：[djangoProject/common/decorators.py](djangoProject/common/decorators.py)。

它的作用是：

- 先用 `JWTAuthentication` 校验请求头里的 Token
- 校验成功后，把 `request.user` 设为当前用户
- 校验失败时，直接返回 `401` 和 `Invalid token`

使用方式：

```python
from djangoProject.common.decorators import require_jwt

@require_jwt
def my_view(request):
    ...
```

### 如何正确请求鉴权接口

如果接口使用了 `require_jwt`，请求时必须先拿到 `access` token，再在请求头里携带：

```bash
curl http://127.0.0.1:8000/o/app/api/test/protected/ \
  -H "Authorization: Bearer 你的access_token"
```

返回规则：

- 不带 Token：返回 `401`
- Token 无效：返回 `401`
- Token 有效：返回 `200`

### 携带 Token 调用普通接口

```bash
curl http://127.0.0.1:8000/o/app/api/todos/ \
  -H "Authorization: Bearer yyy"
```

## Nginx 与部署

如果使用 Nginx 反向代理，请把相关配置放到 `etc/nginx/`，并根据实际域名修改：

- `server_name`
- `BASE_URL`
- `STATIC_URL`
- `CSRF_TRUSTED_ORIGINS`

启动容器：

```bash
docker compose up -d
```

## 常用管理命令

```bash
# 检查项目配置
uv run python manage.py check

# 查看路由
uv run python manage.py show_urls

# 生成迁移
uv run python manage.py makemigrations

# 执行迁移
uv run python manage.py migrate
```

## 常见问题

### 1. 为什么 `api/token/` 不可用？

请确认已经安装 `djangorestframework-simplejwt`。

### 2. 为什么项目能启动，但某些认证功能不存在？

因为当前代码对 `simplejwt` 做了可选导入，避免在轻量环境中直接报错。
