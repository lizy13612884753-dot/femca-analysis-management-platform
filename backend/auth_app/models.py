from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class CustomRole(models.Model):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    permissions = models.JSONField(default=dict, verbose_name='权限配置')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'custom_roles'
        verbose_name = '角色'
        verbose_name_plural = '角色'

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """用户模型"""
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('manager', '项目经理'),
        ('engineer', '工程师'),
        ('operator', '操作员'),
        ('viewer', '查看者'),
    ]
    
    STATUS_CHOICES = [
        ('active', '活跃'),
        ('inactive', '不活跃'),
        ('suspended', '暂停'),
    ]
    
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='名字')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='姓氏')
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='viewer', 
        verbose_name='用户角色'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active', 
        verbose_name='用户状态'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    department = models.CharField(max_length=100, blank=True, verbose_name='部门')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='加入日期')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='最后登录IP')
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 自定义字段用于角色和权限
    groups = models.ManyToManyField(
        CustomRole,
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
        verbose_name='自定义角色'
    )
    user_permissions = models.ManyToManyField(
        'CustomPermission',
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
        verbose_name='自定义权限'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'custom_users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """返回用户的全名"""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_role_display_name(self):
        """获取角色显示名称"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
    
    def get_status_display_name(self):
        """获取状态显示名称"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def update_last_login_info(self, ip_address):
        """更新最后登录信息"""
        self.last_login_ip = ip_address
        self.last_login_time = timezone.now()
        self.save(update_fields=['last_login_ip', 'last_login_time'])


class CustomPermission(models.Model):
    """权限模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='权限名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='权限代码')
    description = models.TextField(blank=True, verbose_name='权限描述')
    module = models.CharField(max_length=50, verbose_name='所属模块')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'custom_permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name