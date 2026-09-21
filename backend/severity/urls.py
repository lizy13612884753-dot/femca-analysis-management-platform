from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SeverityLevelViewSet,
    SeverityIndicatorViewSet,
    SeverityAssessmentViewSet
)

# 创建路由路由器
router = DefaultRouter()

# 注册严酷度等级视图集
router.register(r'levels', SeverityLevelViewSet, basename='severity_level')

# 注册严酷度指标视图集
router.register(r'indicators', SeverityIndicatorViewSet, basename='severity_indicator')

# 注册严酷度评定视图集
router.register(r'assessments', SeverityAssessmentViewSet, basename='severity_assessment')

# 定义严酷度模块的URL路由
urlpatterns = [
    path('', include(router.urls)),
]
