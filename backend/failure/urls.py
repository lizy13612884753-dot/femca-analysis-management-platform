from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FailureModeViewSet,
    FailureCauseViewSet,
    FailureEffectViewSet
)

# 创建路由路由器
router = DefaultRouter()

# 注册故障模式视图集
router.register(r'modes', FailureModeViewSet, basename='failure_mode')

# 注册故障原因视图集
router.register(r'causes', FailureCauseViewSet, basename='failure_cause')

# 注册故障影响视图集
router.register(r'effects', FailureEffectViewSet, basename='failure_effect')

# 定义故障模式模块的URL路由
urlpatterns = [
    path('', include(router.urls)),
]
