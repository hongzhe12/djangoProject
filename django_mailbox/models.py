from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmailConfig(models.Model):
    """邮件配置模型，存储邮件发送相关配置"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="配置名称",
        help_text="用于标识该邮件配置的名称或方案名"
    )
    sender_username = models.EmailField(
        max_length=254,
        verbose_name="发件人邮箱",
        help_text="用于发送邮件的邮箱地址"
    )
    sender_pwd = models.CharField(
        max_length=100,
        verbose_name="发件人密码",
        help_text="发件人邮箱密码或授权码"
    )
    receive_list = models.JSONField(
        default=list,
        verbose_name="收件人列表",
        help_text="接收邮件的邮箱地址列表"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )

    class Meta:
        verbose_name = "邮件配置"
        verbose_name_plural = "邮件配置"
        unique_together = ("sender_username",)  # 确保发件人唯一

    def __str__(self):
        return f"邮件配置: {self.name}"
