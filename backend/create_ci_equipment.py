import os
import django

if os.getenv("CI") != "true":
    raise RuntimeError("This script must only run in CI")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "femca_platform.settings")
django.setup()
from equipment.models import EquipmentType, EquipmentInstance

equipment_type, created = EquipmentType.objects.get_or_create(
    name="CI Test Equipment Type"
)
print(equipment_type.id)
print(created)

equipment_instance, instance_created = EquipmentInstance.objects.get_or_create(
    equipment_type=equipment_type,
    serial_number="CI-001",
    defaults={"name": "CI Test Server"}
)
print(equipment_instance.id)
print(instance_created)