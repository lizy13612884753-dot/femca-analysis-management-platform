from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductHazardAnalysisViewSet

# 创建路由路由器
router = DefaultRouter()

# 注册产品危害度分析视图集
router.register(r'analyses', ProductHazardAnalysisViewSet, basename='product-hazard-analysis')

# 定义产品危害度分析模块的URL路由
urlpatterns = [
    path('', include(router.urls)),
]
