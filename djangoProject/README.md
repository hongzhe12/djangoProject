# Celery 任务调度系统配置指南

## 环境准备

### 依赖安装
```bash
# 安装Redis客户端
pip install redis -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 安装Celery及相关组件
pip install celery django-celery-beat eventlet
```

## 服务启动命令

### Windows 环境下命令（已验证）
```bash
# 启动Celery Worker（任务执行者）
celery -A djangoProject worker -l info -P eventlet

# 启动Celery Beat（任务调度器）
celery -A djangoProject beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Linux/Mac 环境推荐命令
```bash
# 使用多进程模式（CPU密集型任务）
celery -A djangoProject worker --loglevel=info --concurrency=4

# 使用supervisord管理（生产环境）
[program:celery_worker]
command=celery -A djangoProject worker -l info
autostart=true
autorestart=true
```

## 定时任务管理

### 动态添加定时任务
```python
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from datetime import datetime

# 方式1：使用Crontab表达式
def create_crontab_task():
    # 创建每天8点的调度规则
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='8',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone='Asia/Shanghai'
    )

    PeriodicTask.objects.create(
        crontab=schedule,
        name='每日邮件报告',
        task='django_mail.tasks.send_daily_report',
        args='[]',
        kwargs='{}',
        enabled=True
    )

# 方式2：使用间隔时间
def create_interval_task():
    # 每30分钟执行一次
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name='数据同步任务',
        task='data.tasks.sync_data',
        start_time=datetime.now()
    )
```

### 任务管理API
```python
# 启用/禁用任务
task = PeriodicTask.objects.get(name='每日邮件报告')
task.enabled = False  # 禁用任务
task.save()

# 立即执行一次任务
from celery.execute import send_task
send_task('django_mail.tasks.send_daily_report')
```

## 配置建议

### settings.py 关键配置
```python
# Celery配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

## 监控与管理

### 常用监控命令
```bash
# 检查注册任务
docker exec mysite-celerybeat celery -A djangoProject inspect registered

# 查看Worker状态
celery -A djangoProject status

# 查看活动任务
celery -A djangoProject inspect active

# 查看已注册任务
celery -A djangoProject inspect registered
```

### Flower 监控工具
```bash
# 安装监控面板
pip install flower

# 启动监控服务
celery -A djangoProject flower --port=5555
```
访问 `http://localhost:5555` 查看任务监控面板

## 最佳实践

1. **任务设计原则**：
   - 保持任务短小精悍
   - 添加任务超时设置
   - 实现任务幂等性

2. **异常处理**：
```python
@app.task(bind=True, max_retries=3)
def send_email(self, email_id):
    try:
        # 发送邮件逻辑
    except SMTPException as exc:
        self.retry(exc=exc, countdown=60)
```

3. **性能优化**：
   - I/O密集型任务使用 eventlet/gevent
   - CPU密集型任务使用多进程
   - 合理设置并发数（`--concurrency`）