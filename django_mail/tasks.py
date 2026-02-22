import datetime

from celery import shared_task
from .utils import send_email_with_attachment

@shared_task(bind=True, max_retries=3)
def send_email(self, subject="每日报告", content=datetime.datetime.today().strftime("%Y年%m月%d日 %H:%M:%S")):
    try:
        send_email_with_attachment(subject, content)
        return "邮件发送成功"
    except Exception as e:
        self.retry(exc=e, countdown=60)  # 失败后60秒重试
