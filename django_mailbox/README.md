## 使用方法

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from django_mailbox.utils import send_email_with_attachment

if __name__ == "__main__":
    subject = "定时邮件测试"
    content = "这是一封由定时任务发送的测试邮件。"
    send_email_with_attachment(subject, content)
```

## cookiecutter 打包配置
```bash
pip uninstall django-mailbox

cookiecutter https://github.com/hongzhe12/cookiecutter-djangopackage.git

Hongzhe
hongzhe2022@163.com
hongzhe12
Django Mailbox
django-mailbox
django_mailbox
MailBoxConfig
这是一个用于配置和发送邮件的 Django 应用，支持邮箱配置管理、表单验证及带附件的邮件发送功能。
EmailConfig
4.0,4.1,4.2
1.0.0
N
1
```

## MANIFEST.in 配置
```bash
include AUTHORS.rst
include CONTRIBUTING.rst
include HISTORY.rst
include LICENSE
include README.rst
include requirements.txt
recursive-include django_mailbox *.html *.png *.gif *js *.css *jpg *jpeg *svg *py
```


## 编译python软件包
```bash
set PYTHONUTF8=1
python -m build
```

## 安装使用
```bash
pip install dist\django_mailbox-1.0.0-py2.py3-none-any.whl
```
