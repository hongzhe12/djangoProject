from rest_framework import serializers

# 请替换为实际的模型导入
from .models import (
    EmailConfig
)



class BaseMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # 由子类指定
        fields = '__all__'


def get_metric_serializer(model_cls):
    '''
    根据模型动态生成序列化器
    '''
    class DynamicMetricSerializer(BaseMetricSerializer):
        class Meta:
            model = model_cls
            fields = '__all__'

    return DynamicMetricSerializer


# 自动生成的模型序列化器

class EmailConfigSerializer(BaseMetricSerializer):
    class Meta:
        model = EmailConfig
        fields = '__all__'


class SendMailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=200)
    content = serializers.CharField()
    filepath = serializers.CharField(required=False, allow_blank=True, allow_null=True)

