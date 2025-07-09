from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import EmailConfig


class EmailConfigForm(forms.ModelForm):
    sender_pwd = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        label="发件人密码",
        required=True,
        help_text="请输入发件人邮箱密码或授权码"
    )

    receive_list = forms.CharField(
        widget=forms.Textarea,
        label="收件人邮箱列表",
        help_text="每行输入一个邮箱地址",
        required=True
    )

    class Meta:
        model = EmailConfig
        fields = ['sender_username', 'sender_pwd', 'receive_list', 'name']
        labels = {
            'sender_username': '发件人邮箱',
            'sender_pwd': '发件人密码',  # 新增标签定义
        }
        field_classes = {
            'sender_username': forms.EmailField,  # 使用内置EmailField验证
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.receive_list:
            self.initial['receive_list'] = '\n'.join(self.instance.receive_list)
        if self.instance and self.instance.sender_pwd:
            self.initial['sender_pwd'] = self.instance.sender_pwd  # 改为sender_pwd

    def _validate_email(self, email):
        """验证单个邮箱地址"""
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(f"邮箱格式不正确: {email}")
        return email

    def clean_receive_list(self):
        """验证收件人列表"""
        receive_text = self.cleaned_data.get('receive_list', '').strip()
        if not receive_text:
            raise forms.ValidationError("请输入至少一个收件人邮箱地址")

        # 分割并过滤空行
        emails = [email.strip() for email in receive_text.splitlines() if email.strip()]

        # 验证所有邮箱
        for email in emails:
            self._validate_email(email)

        return emails

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.receive_list = self.cleaned_data['receive_list']
        instance.sender_pwd = self.cleaned_data['sender_pwd']
        if commit:
            instance.save()
        return instance
