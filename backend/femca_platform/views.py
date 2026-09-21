from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os

def index(request, path=None):
    # 提供前端构建后的index.html文件
    index_path = os.path.join(settings.STATIC_ROOT, 'dist', 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HttpResponse(html_content)
    return HttpResponse("前端资源未找到", status=404)
