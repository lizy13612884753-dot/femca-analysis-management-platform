from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, CustomRole, CustomPermission


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'department']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码和确认密码不匹配")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if user.status == 'suspended':
                raise serializers.ValidationError('账户已被暂停')
            if user.status == 'inactive':
                raise serializers.ValidationError('账户已停用')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('必须提供用户名和密码')


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role_display = serializers.CharField(source='get_role_display_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_display',
                 'status', 'status_display', 'phone', 'department', 'last_login_ip', 
                 'last_login_time', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined', 'last_login_ip', 'last_login_time']


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    role_display = serializers.CharField(source='get_role_display_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_display',
                 'status', 'status_display', 'phone', 'department', 'last_login_ip', 
                 'last_login_time', 'date_joined', 'is_active', 'is_staff', 'is_superuser']


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    
    class Meta:
        model = CustomRole
        fields = ['id', 'name', 'description', 'permissions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    
    class Meta:
        model = CustomPermission
        fields = ['id', 'name', 'code', 'description', 'module', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码不正确')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('新密码和确认密码不匹配')
        return attrs