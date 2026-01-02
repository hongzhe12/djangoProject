# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /code

COPY requirements.txt .

# 复制项目代码
COPY . .


# 在线安装Python依赖
RUN pip install uv -i http://pypi.doubanio.com/simple/
RUN uv pip install --system --no-cache-dir -r requirements.txt -i http://pypi.doubanio.com/simple/

# 离线安装Python依赖
# RUN pip install --no-index --find-links=/code/python_packages/ -r requirements.txt


# 设置环境变量
ENV DJANGO_SETTINGS_MODULE=djangoProject.settings



