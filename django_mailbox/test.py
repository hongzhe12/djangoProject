import os
from jinja2 import Template



def generate_serializers_file(models, output_path='serializers.py', app_name=None):
    """
    生成 DRF 序列化器文件的通用脚本

    参数:
        models: 模型列表，每个元素是模型类或模型类名字符串
        output_path: 输出文件路径
        app_name: 应用名(用于import路径)
    """
    # 模板定义
    template_str = """\
from rest_framework import serializers
{% if app_name %}
from {{ app_name }}.models import (
    {% for model in models %}{{ model }}{% if not loop.last %},{% endif %}{% endfor %}
)
{% else %}
# 请替换为实际的模型导入
from .models import (
    {% for model in models %}{{ model }}{% if not loop.last %},{% endif %}{% endfor %}
)
{% endif %}


class BaseMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # 由子类指定
        fields = '__all__'


def get_metric_serializer(model):
    '''
    根据模型动态生成序列化器
    '''
    class DynamicMetricSerializer(BaseMetricSerializer):
        class Meta:
            model = model
            fields = '__all__'

    return DynamicMetricSerializer


# 自动生成的模型序列化器
{% for model in models %}
class {{ model }}Serializer(BaseMetricSerializer):
    class Meta:
        model = {{ model }}
        fields = '__all__'

{% endfor %}
"""

    # 处理模型名称
    model_names = [model.__name__ if not isinstance(model, str) else model for model in models]

    # 渲染模板
    template = Template(template_str)
    content = template.render(
        models=model_names,
        app_name=app_name
    )

    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"序列化器文件已生成: {output_path}")


def generate_views_file(models, output_path='views.py', app_name=None, serializer_import_path='.serializers'):
    """
    生成 DRF 视图文件的通用脚本

    参数:
        models: 模型列表，每个元素是模型类或模型类名字符串
        output_path: 输出文件路径
        app_name: 应用名(用于import路径)
        serializer_import_path: 序列化器的导入路径
    """
    # 模板定义
    template_str = """\
from rest_framework import viewsets
{% if app_name %}
from {{ app_name }}.models import (
    {% for model in models %}{{ model }}{% if not loop.last %},{% endif %}{% endfor %}
)
{% else %}
# 请替换为实际的模型导入
from .models import (
    {% for model in models %}{{ model }}{% if not loop.last %},{% endif %}{% endfor %}
)
{% endif %}
from {{ serializer_import_path }} import (
    {% for model in models %}{{ model }}Serializer{% if not loop.last %},{% endif %}{% endfor %}
)


class BaseModelViewSet(viewsets.ModelViewSet):
    '''
    基础视图集，可在此添加通用逻辑
    '''
    pass


# 自动生成的模型视图集
{% for model in models %}
class {{ model }}ViewSet(BaseModelViewSet):
    queryset = {{ model }}.objects.all()
    serializer_class = {{ model }}Serializer

{% endfor %}
"""

    # 处理模型名称
    model_names = [model.__name__ if not isinstance(model, str) else model for model in models]

    # 渲染模板
    template = Template(template_str)
    content = template.render(
        models=model_names,
        app_name=app_name,
        serializer_import_path=serializer_import_path
    )

    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"视图文件已生成: {output_path}")


def generate_urls_file(models, output_path='urls.py', app_name=None, views_import_path='.views'):
    """
    生成 DRF 路由文件的通用脚本

    参数:
        models: 模型列表，每个元素是模型类或模型类名字符串
        output_path: 输出文件路径
        app_name: 应用名(用于import路径)
        views_import_path: 视图的导入路径
    """
    # 模板定义
    template_str = """\
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from {{ views_import_path }} import (
    {% for model in models %}{{ model }}ViewSet{% if not loop.last %},{% endif %}{% endfor %}
)


router = DefaultRouter()

# 自动注册视图集路由
{% for model in models %}
router.register(r'{{ model|lower }}', {{ model }}ViewSet, basename='{{ model|lower }}')
{% endfor %}

urlpatterns = [
    path('', include(router.urls)),

    # 在此添加其他自定义路由
]
"""

    # 处理模型名称
    model_names = [model.__name__ if not isinstance(model, str) else model for model in models]

    # 渲染模板
    template = Template(template_str)
    content = template.render(
        models=model_names,
        app_name=app_name,
        views_import_path=views_import_path
    )

    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"路由文件已生成: {output_path}")


def generate_all(models, output_dir='.', app_name=None):
    """
    一次性生成序列化器、视图和URL文件

    参数:
        models: 模型列表
        output_dir: 输出目录
        app_name: 应用名
    """
    generate_serializers_file(models, os.path.join(output_dir, 'serializers.py'), app_name)
    generate_views_file(models, os.path.join(output_dir, 'views.py'), app_name)
    generate_urls_file(models, os.path.join(output_dir, 'urls.py'), app_name)
    print(f"所有文件已生成到目录: {output_dir}")


# 使用示例
if __name__ == "__main__":
    # 示例1: 直接使用模型类名列表
    models = [
        'EmailConfig',
    ]

    # 生成到当前目录
    generate_all(models)

    # 示例2: 如果你有实际的模型类，可以这样使用
    # from yourapp.models import YourModel1, YourModel2