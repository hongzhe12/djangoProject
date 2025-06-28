import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from django_mailbox.utils import send_email_with_attachment

if __name__ == "__main__":
    subject = "定时邮件测试"
    content = "这是一封由定时任务发送的测试邮件。"
    send_email_with_attachment(subject, content)