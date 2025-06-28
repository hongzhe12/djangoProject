from rest_framework import viewsets

# 请替换为实际的模型导入
from .serializers import (
    EmailConfigSerializer
)

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .form import EmailConfigForm
from .models import EmailConfig


class BaseModelViewSet(viewsets.ModelViewSet):
    '''
    基础视图集，可在此添加通用逻辑
    '''
    pass


# 自动生成的模型视图集

class EmailConfigViewSet(BaseModelViewSet):
    queryset = EmailConfig.objects.all()
    serializer_class = EmailConfigSerializer




@csrf_exempt
def index(request):
    # 尝试获取最新的邮件配置，若无则创建新实例
    try:
        email_config = EmailConfig.objects.latest('updated_at')
    except EmailConfig.DoesNotExist:
        email_config = None

    # 处理POST请求（表单提交）
    if request.method == 'POST':
        form = EmailConfigForm(request.POST, instance=email_config)
        # 添加调试输出
        print("表单是否有效:", form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, "邮件配置已成功更新！")
            return redirect('email_config')
        else:
            print("表单错误:", form.errors)
    else:
        # 处理GET请求，初始化表单并加载现有数据
        form = EmailConfigForm(instance=email_config)

    # 渲染页面，传递表单实例到模板
    return render(request, "django_mailbox/email.html", {'form': form})
