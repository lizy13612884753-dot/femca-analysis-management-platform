from django.core.management.base import BaseCommand
from failure.models import FailureMode
from auth_app.models import CustomUser

class Command(BaseCommand):
    help = '检查所有表中的异常数据'

    def handle(self, *args, **options):
        self.stdout.write("=== 检查故障模式表 ===")
        failure_modes = FailureMode.objects.all()
        self.stdout.write(f"总记录数: {failure_modes.count()}")

        abnormal = failure_modes.filter(
            name__icontains='弦'
        ) | failure_modes.filter(
            name__icontains='约会'
        ) | failure_modes.filter(
            name__icontains='智'
        ) | failure_modes.filter(
            description__icontains='弦'
        ) | failure_modes.filter(
            description__icontains='约会'
        ) | failure_modes.filter(
            description__icontains='智'
        )

        if abnormal.exists():
            self.stdout.write(f"\n发现 {abnormal.count()} 条异常记录:")
            for data in abnormal:
                self.stdout.write(f"ID: {data.id}, 名称: {data.name}, 描述: {data.description}")
        else:
            self.stdout.write("\n未发现异常记录")

        self.stdout.write("\n=== 检查用户表 ===")
        users = CustomUser.objects.all()
        self.stdout.write(f"总记录数: {users.count()}")

        abnormal_users = users.filter(
            username__icontains='弦'
        ) | users.filter(
            username__icontains='约会'
        ) | users.filter(
            username__icontains='智'
        ) | users.filter(
            first_name__icontains='弦'
        ) | users.filter(
            first_name__icontains='约会'
        ) | users.filter(
            first_name__icontains='智'
        ) | users.filter(
            last_name__icontains='弦'
        ) | users.filter(
            last_name__icontains='约会'
        ) | users.filter(
            last_name__icontains='智'
        )

        if abnormal_users.exists():
            self.stdout.write(f"\n发现 {abnormal_users.count()} 条异常用户记录:")
            for user in abnormal_users:
                self.stdout.write(f"ID: {user.id}, 用户名: {user.username}, 姓: {user.first_name}, 名: {user.last_name}")
        else:
            self.stdout.write("\n未发现异常用户记录")