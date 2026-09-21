from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DashboardViewSet

# 创建路由路由器
router = DefaultRouter()

# 注册仪表盘视图集
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# 定义仪表盘模块的URL路由
urlpatterns = [
    path('', include(router.urls)),
]
