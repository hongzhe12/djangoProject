from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

class EmailConfig(models.Model):
    """邮件配置模型，存储邮件发送相关配置"""
    name = models.CharField(
        max_length=100,
        verbose_name="配置名称",
        help_text="用于标识该邮件配置的名称或方案名",
        blank=True
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

    def __str__(self):
        return f"邮件配置: {self.name}"


import uuid

class BatchTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    total_questions = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def progress_percent(self):
        if self.total_questions == 0:
            return 0
        return int((self.completed_count + self.error_count) / self.total_questions * 100)

class TaskItem(models.Model):
    STATUS_CHOICES = [
        ('processing', '处理中'),
        ('success', '成功'),
        ('error', '失败'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_task = models.ForeignKey(BatchTask, related_name='items', on_delete=models.CASCADE)
    question = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    result = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']