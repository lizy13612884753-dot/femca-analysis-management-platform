from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HazardAnalysisParameterViewSet,
    FailureModeHazardAnalysisViewSet
)

# 创建路由路由器
router = DefaultRouter()

# 注册危害度参数视图集
router.register(r'parameters', HazardAnalysisParameterViewSet, basename='hazard-parameter')

# 注册故障模式危害度分析视图集
router.register(r'analyses', FailureModeHazardAnalysisViewSet, basename='hazard-analysis')

# 定义故障模式危害度分析模块的URL路由
urlpatterns = [
    path('', include(router.urls)),
]
