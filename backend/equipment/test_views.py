from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EquipmentInstance

@api_view(['GET'])
def test_equipment_instances(request):
    """测试设备实例API端点"""
    # 获取所有设备实例
    instances = EquipmentInstance.objects.all()
    
    # 手动构建响应数据
    results = []
    for instance in instances:
        result = {
            'id': instance.id,
            'name': instance.name,
            'function_description': instance.function_description  # 确保包含这个字段
        }
        results.append(result)
    
    return Response({'results': results, 'count': len(results)})
