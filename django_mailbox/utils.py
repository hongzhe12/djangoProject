import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django_mailbox.models import EmailConfig


def send_email_with_attachment(subject: str, content: str, filepath: str = None):
    email_config = EmailConfig.objects.latest('updated_at')
    _user = email_config.sender_username
    _pwd = email_config.sender_pwd
    recipients = email_config.receive_list

    # 判断邮箱类型
    if _user.endswith('@qq.com'):
        smtp_server = "smtp.qq.com"
        smtp_port = 465
    elif _user.endswith('@163.com'):
        smtp_server = "smtp.163.com"
        smtp_port = 465
    else:
        raise ValueError("暂不支持该邮箱类型")

    for recipient in recipients:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.ehlo(smtp_server)
        smtp.login(_user, _pwd)

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = _user
        msg["To"] = recipient  # 单个收件人

        part = MIMEText(content, _charset='utf-8')
        msg.attach(part)

        if filepath is None:
            print("没有附件")
        else:
            part = MIMEApplication(open(filepath, 'rb').read())
            filename = os.path.split(filepath)[-1]
            part.add_header('Content-Disposition', 'attachment',
                            filename=filename)
            msg.attach(part)

        smtp.sendmail(_user, recipient, msg.as_string())

        print(f"已发送给: {recipient}")
        time.sleep(1)  # 适当间隔避免发送频率过高
        smtp.quit()
        print(f"全部发送完成！共发送 {len(recipients)} 人")
