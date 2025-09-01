from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django_mailbox.form import EmailConfigForm
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from .tasks import get_sparkai_response_task
import json
import uuid

from .models import EmailConfig
# 请替换为实际的模型导入
from .serializers import (
    EmailConfigSerializer,
    SendMailSerializer
)
from .utils import send_email_with_attachment
import logging

logger = logging.getLogger(__name__)

class BaseModelViewSet(viewsets.ModelViewSet):
    '''
    基础视图集，可在此添加通用逻辑
    '''
    pass


# 自动生成的模型视图集

class EmailConfigViewSet(BaseModelViewSet):
    queryset = EmailConfig.objects.all()
    serializer_class = EmailConfigSerializer


@csrf_exempt  # 临时保留以便调试
def index(request):
    try:
        email_config = EmailConfig.objects.latest('updated_at')
        logger.info(f"现有配置: {email_config.__dict__}")
    except EmailConfig.DoesNotExist:
        email_config = None
        logger.info("无现有配置")

    if request.method == 'POST':
        logger.info(f"收到POST数据: {request.POST}")
        form = EmailConfigForm(request.POST, instance=email_config)
        
        if form.is_valid():
            instance = form.save()
            logger.info(f"保存成功! 新实例ID: {instance.id}")
            messages.success(request, "配置已保存")
            return redirect('django_mailbox:email')
        else:
            logger.error(f"表单无效: {form.errors}")
    else:
        form = EmailConfigForm(instance=email_config)

    return render(request, "django_mailbox/email.html", {'form': form})


class SendMailAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        # 打印当前路径
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            content = serializer.validated_data['content']
            filepath = serializer.validated_data.get('filepath')
            # 打印当前路径
            if filepath:
                import os
                print('邮件附件绝对路径:', os.path.abspath(filepath))
            try:
                send_email_with_attachment(subject, content, filepath)
                return Response({"detail": "邮件发送成功"})
            except Exception as e:
                return Response({"detail": f"邮件发送失败: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@csrf_exempt
@require_POST
def start_sparkai_chat(request):
    """
    启动异步AI聊天任务
    """
    try:
        data = json.loads(request.body)
        user_input = data.get('message', '')
        
        if not user_input:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        
        # 启动异步任务
        get_sparkai_response_task.delay(user_input, task_id)
        
        # 立即返回任务ID
        return JsonResponse({
            'status': 'processing',
            'task_id': task_id,
            'message': 'Request is being processed asynchronously'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def check_sparkai_result(request, task_id):
    """
    检查任务结果
    """
    result = cache.get(f'sparkai_result_{task_id}')
    
    if not result:
        return JsonResponse({
            'status': 'processing',
            'message': 'Task not found or still processing'
        }, status=404)
    
    if result['status'] == 'success':
        return JsonResponse({
            'status': 'completed',
            'result': result['result'],
            'completed_at': result['completed_at']
        })
    else:
        return JsonResponse({
            'status': 'error',
            'error': result['error'],
            'completed_at': result['completed_at']
        }, status=500)