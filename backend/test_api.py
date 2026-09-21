#!/usr/bin/env python
"""测试后端API是否正确返回failure_mode_name字段"""

import os
import django
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca.settings')
django.setup()

from auth_app.models import CustomUser

# 创建测试用户
user, created = CustomUser.objects.get_or_create(email='test@example.com')
if created:
    user.set_password('testpassword')
    user.save()

# 创建测试客户端
client = Client()

# 获取JWT token
refresh = RefreshToken.for_user(user)
token = str(refresh.access_token)

# 测试API
response = client.get(
    '/api/severity/assessments/',
    HTTP_AUTHORIZATION=f'Bearer {token}'
)

print('API响应状态码:', response.status_code)
print('API响应内容:', response.json())
