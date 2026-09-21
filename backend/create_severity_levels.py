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
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    # 获取admin用户
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
    except Exception as e:
        print(f"创建admin用户失败: {e}")
        admin_user = None
    
    # 定义需要创建的严酷度等级
    severity_levels_data = [
        {
            'level': 'Ⅰ',
            'name': '灾难性',
            'description': '导致人员伤亡或系统完全失效',
            'criteria': '系统或设备的故障会导致人员死亡或严重伤害，或者导致系统完全失效无法修复',
            'score': 100.00,
            'is_active': True
        },
        {
            'level': 'Ⅱ',
            'name': '严重',
            'description': '导致系统性能严重下降，影响安全',
            'criteria': '系统或设备的故障会导致系统性能严重下降，需要立即停机修复，可能影响安全',
            'score': 75.00,
            'is_active': True
        },
        {
            'level': 'Ⅲ',
            'name': '中等',
            'description': '导致系统性能下降，但不影响安全',
            'criteria': '系统或设备的故障会导致系统性能下降，但可以继续运行，不影响安全',
            'score': 50.00,
            'is_active': True
        },
        {
            'level': 'Ⅳ',
            'name': '轻微',
            'description': '对系统性能影响很小',
            'criteria': '系统或设备的故障对系统性能影响很小，几乎不影响系统运行',
            'score': 25.00,
            'is_active': True
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for level_data in severity_levels_data:
        # 检查是否已存在该等级
        level, created = SeverityLevel.objects.update_or_create(
            level=level_data['level'],
            defaults={
                'name': level_data['name'],
                'description': level_data['description'],
                'criteria': level_data['criteria'],
                'score': level_data['score'],
                'is_active': level_data['is_active'],
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"成功创建SeverityLevel: {level.level} - {level.name}")
            created_count += 1
        else:
            print(f"成功更新SeverityLevel: {level.level} - {level.name}")
            updated_count += 1
    
    print(f"\n操作完成: 创建了 {created_count} 条记录，更新了 {updated_count} 条记录")
    
    # 验证结果
    print("\n当前SeverityLevel数据:")
    for level in SeverityLevel.objects.all():
        print(f"ID: {level.id}, Level: {level.level}, Name: {level.name}, Score: {level.score}")

if __name__ == "__main__":
    main()
