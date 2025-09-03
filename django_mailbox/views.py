from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django_mailbox.form import EmailConfigForm
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from .tasks import get_sparkai_response_task
import json
import time
import os
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

        
        # 启动异步任务
        get_sparkai_response_task.delay(user_input)
        
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





import datetime

def timestamp_to_human(timestamp):
    # 转换为UTC时间
    utc_time = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    # 转换为北京时间 (UTC+8)
    beijing_time = utc_time.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    
    # 格式化输出
    formatted_time = beijing_time.strftime("%Y年%m月%d日 %H:%M:%S")
    
    return formatted_time


def batch_tasks_view(request):
    """
    批量任务提交界面 - 支持文件上传
    """
    if request.method == 'POST':
        questions = []
        
        # 处理文件上传
        uploaded_file = request.FILES.get('questions_file')
        if uploaded_file:
            try:
                # 读取上传的文件内容
                content = uploaded_file.read().decode('utf-8')
                # 按行分割，过滤空行
                file_questions = [line.strip() for line in content.split('\n') if line.strip()]
                questions.extend(file_questions)
            except Exception as e:
                messages.error(request, f'文件读取失败: {str(e)}')
                return redirect('django_mailbox:batch_tasks')
        
        # 处理手动输入的问题
        for key in request.POST:
            if key.startswith('question_') and request.POST[key].strip():
                questions.append(request.POST[key].strip())
        
        if not questions:
            messages.error(request, '请至少输入一个有效的问题或上传文件')
            return redirect('django_mailbox:batch_tasks')
        
        # 限制最大问题数量，避免性能问题
        if len(questions) > 100:
            messages.warning(request, f'问题数量超过100个，将只处理前100个问题')
            questions = questions[:100]
        
        # 生成任务ID列表
        task_ids = []
        for question in questions:
            task_id = str(uuid.uuid4())
            task_ids.append(task_id)
            # 启动异步任务
            get_sparkai_response_task.delay(question, task_id)
        
        # 存储任务信息到session
        request.session['last_batch_tasks'] = {
            'task_ids': task_ids,
            'questions': questions,
            'submitted_at': time.time(),
            'total_questions': len(questions)
        }
        
        messages.success(request, f'已提交 {len(questions)} 个任务，请查看任务状态')
        return redirect('django_mailbox:task_status')
    
    # GET请求显示空表单
    return render(request, "django_mailbox/batch_tasks.html")

def task_status(request):
    """
    任务状态查看页面 - 添加分页功能
    """
    task_info = request.session.get('last_batch_tasks', {})
    task_ids = task_info.get('task_ids', [])
    questions = task_info.get('questions', [])
    total_questions = task_info.get('total_questions', 0)
    
    results = []
    completed_count = 0
    processing_count = 0
    error_count = 0
    
    for i, task_id in enumerate(task_ids):
        result = cache.get(f'sparkai_result_{task_id}')
        status = result['status'] if result else 'processing'
        
        if status == 'success':
            completed_count += 1
        elif status == 'error':
            error_count += 1
        else:
            processing_count += 1
        

        
        results.append({
            'question': questions[i] if i < len(questions) else '未知问题',
            'task_id': task_id,
            'status': status,
            'result': result.get('result') if result else None,
            'error': result.get('error') if result else None,
            'completed_at': timestamp_to_human(result.get('completed_at')) if result else None
        })
    
    # 计算进度百分比
    progress_percent = int((completed_count + error_count) / len(task_ids) * 100) if task_ids else 0
    
    per_page = int(request.GET.get('per_page', 1))
    per_page = min(per_page, 20)  # 限制最大每页20条

    # 添加分页功能
    paginator = Paginator(results, per_page)  # 每页显示per_page条
    page_number = request.GET.get('page', 1)
    
    try:
        page_results = paginator.page(page_number)
    except PageNotAnInteger:
        page_results = paginator.page(1)
    except EmptyPage:
        page_results = paginator.page(paginator.num_pages)
    
    context = {
        'results': page_results,  # 使用分页后的结果
        'total_count': len(task_ids),
        'completed_count': completed_count,
        'processing_count': processing_count,
        'error_count': error_count,
        'progress_percent': progress_percent,
        'submitted_at': task_info.get('submitted_at'),
        'total_questions': total_questions
    }
    
    return render(request, "django_mailbox/task_status.html", context)