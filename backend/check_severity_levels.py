#!/usr/bin/env python

import os
import sys

# 添加Django项目的根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')

# 导入Django设置
import django
django.setup()

# 导入模型
from severity.models import SeverityLevel

# 获取所有SeverityLevel数据
severity_levels = SeverityLevel.objects.all()

print("SeverityLevel数据:")
for level in severity_levels:
    print(f"ID: {level.id}, Level: {level.level}, Name: {level.name}, Score: {level.score}")

print(f"\n总共有 {len(severity_levels)} 条SeverityLevel记录")
