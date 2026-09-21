from equipment.models import EquipmentInstance

# 获取所有设备实例
instances = EquipmentInstance.objects.all()
print('设备实例数量:', instances.count())

# 打印前5个实例的功能描述
for instance in instances[:5]:
    print(f'ID: {instance.id}')
    print(f'名称: {instance.name}')
    print(f'功能描述: "{instance.function_description}"')
    print(f'功能描述长度: {len(instance.function_description) if instance.function_description else 0}')
    print('-' * 30)