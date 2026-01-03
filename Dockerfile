# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 创建/etc/apt/sources.list
RUN touch /etc/apt/sources.list

# 设置清华源（Debian 11 bullseye github actions 构建无须换源）
# RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
#     && sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 安装同步工具rsync并清理缓存
RUN apt update \
    && apt install -y --no-install-recommends rsync \
    && rm -rf /var/lib/apt/lists/*

# 安装git
RUN apt update \
    && apt upgrade -y \
    && apt autoremove -y \
    && apt clean

# 设置工作目录
WORKDIR /code

COPY requirements.txt .

# 复制项目代码
COPY . .


# 在线安装Python依赖
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 离线安装Python依赖
# RUN pip install --no-index --find-links=/code/python_packages/ -r requirements.txt



# 设置环境变量
ENV DJANGO_SETTINGS_MODULE=djangoProject.settings



