# 使用官方 Python 运行时作为基础镜像 (尝试使用 DockerProxy 镜像)
FROM docker.m.daocloud.io/library/python:3.9-slim
# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 安装系统依赖（配置国内镜像源以加速 apt-get）
# 尝试兼容新旧两种 Debian 软件源格式
RUN if [ -f /etc/apt/sources.list ]; then \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list; \
    fi && \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露 Flask 运行的端口
EXPOSE 5001

# 使用 Gunicorn 运行应用
# -w 4: 启动 4 个工作进程
# -b 0.0.0.0:5001: 绑定到所有接口的 5001 端口
# web_app:app: 模块名:应用实例名
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "web_app:app"]
