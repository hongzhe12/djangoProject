import datetime

from celery import shared_task
from .utils import send_email_with_attachment

from django.core.cache import cache
import time
import uuid

@shared_task(bind=True, max_retries=3)
def send_daily_report(self, subject="每日报告", content=datetime.datetime.today().strftime("%Y年%m月%d日 %H:%M:%S")):
    try:
        send_email_with_attachment(subject, content)
        return "邮件发送成功"
    except Exception as e:
        self.retry(exc=e, countdown=60)  # 失败后60秒重试

@shared_task(bind=True, max_retries=3)
def get_sparkai_response_task(self, user_input, task_id=None):
    """
    异步获取星火大模型回复的任务
    """
    if task_id is None:
        # 使用self.request.id获取Celery的task_id
        task_id = self.request.id
        
        # task_id = str(uuid.uuid4())
    
    try:
        # 延迟导入，避免循环导入问题
        from sparkai.core.outputs import LLMResult
        from sparkai.llm.llm import ChatSparkLLM
        from sparkai.core.messages import ChatMessage
        
        SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
        SPARKAI_APP_ID = 'd556db59'
        SPARKAI_API_SECRET = 'ZWZlZmMzMWIyZDg5ZGI5YzdhMjAzZTFk'
        SPARKAI_API_KEY = '6e8ce352b289b970b4fe335a426f0320'
        SPARKAI_DOMAIN = '4.0Ultra'

        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
            request_timeout=120
        )
        
        messages = [ChatMessage(role="user", content=user_input)]
        
        # 执行模型调用
        result = spark.generate([messages])
        
        # 处理结果
        if isinstance(result, LLMResult) and result.generations:
            reply_text = result.generations[0][0].text
            
            # 将结果存储到缓存中
            cache.set(f'sparkai_result_{task_id}', {
                'status': 'success',
                'result': reply_text,
                'completed_at': time.time()
            }, 600)
            
            return reply_text
        else:
            raise ValueError("Invalid response format from SparkAI")
            
    except Exception as e:
        # 记录错误信息
        error_msg = str(e)
        cache.set(f'sparkai_result_{task_id}', {
            'status': 'error',
            'error': error_msg,
            'completed_at': time.time()
        }, 600)
        
        # 重试逻辑
        try:
            self.retry(exc=e, countdown=60 * self.request.retries)
        except self.MaxRetriesExceededError:
            return None