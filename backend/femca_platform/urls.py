from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os
from femca_platform.views import index
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from auth_app.views import (
    RegisterViewSet, LoginViewSet, LogoutViewSet, 
    UserViewSet, RoleViewSet, PermissionViewSet
)
from equipment.views import EquipmentTypeViewSet, EquipmentInstanceViewSet
from failure.views import FailureModeViewSet, FailureCauseViewSet, FailureEffectViewSet
from detection.views import (
    DetectionMethodViewSet, DetectionRatingViewSet, FailureModeDetectionViewSet
)
from compensation.views import (
    CompensationMeasureViewSet, EffectivenessEvaluationViewSet, FailureModeCompensationViewSet
)
from severity.views import (
    SeverityLevelViewSet, SeverityIndicatorViewSet, SeverityAssessmentViewSet
)
from failure_analysis.views import (
    HazardAnalysisParameterViewSet, FailureModeHazardAnalysisViewSet
)
from product_analysis.views import (
    ProductHazardAnalysisViewSet
)
from dashboard.views import (
    DashboardViewSet
)
from users.views import UserSettingsViewSet

router = DefaultRouter()
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'auth/login', LoginViewSet, basename='login')
router.register(r'users/settings', UserSettingsViewSet, basename='user-settings')
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'equipment/types', EquipmentTypeViewSet, basename='equipment-type')
router.register(r'equipment/instances', EquipmentInstanceViewSet, basename='equipment-instance')
router.register(r'detection/methods', DetectionMethodViewSet, basename='detection-method')
router.register(r'detection/ratings', DetectionRatingViewSet, basename='detection-rating')
router.register(r'detection/failure-mode', FailureModeDetectionViewSet, basename='failure-mode-detection')
router.register(r'compensation/measures', CompensationMeasureViewSet, basename='compensation-measure')
router.register(r'compensation/evaluations', EffectivenessEvaluationViewSet, basename='effectiveness-evaluation')
router.register(r'compensation/failure-mode', FailureModeCompensationViewSet, basename='failure-mode-compensation')
router.register(r'failure/modes', FailureModeViewSet, basename='failure-mode')
router.register(r'failure/causes', FailureCauseViewSet, basename='failure-cause')
router.register(r'failure/effects', FailureEffectViewSet, basename='failure-effect')
router.register(r'severity/levels', SeverityLevelViewSet, basename='severity-level')
router.register(r'severity/indicators', SeverityIndicatorViewSet, basename='severity-indicator')
router.register(r'severity/assessments', SeverityAssessmentViewSet, basename='severity-assessment')
router.register(r'failure-analysis/parameters', HazardAnalysisParameterViewSet, basename='hazard-parameter')
router.register(r'failure-analysis/analyses', FailureModeHazardAnalysisViewSet, basename='hazard-analysis')
router.register(r'product-analysis/analyses', ProductHazardAnalysisViewSet, basename='product-hazard-analysis')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# 添加测试API端点
from equipment.test_views import test_equipment_instances

urlpatterns = [
    path('admin/', admin.site.urls),
    # 测试API端点
    path('api/test-equipment-instances/', test_equipment_instances),
    path('test-equipment-instances/', test_equipment_instances),
    # 为了兼容前端请求，同时暴露有/api前缀和没有/api前缀的API路由
    path('api/', include(router.urls)),
    # 为了兼容前端请求，同时暴露有/api前缀和没有/api前缀的API路由
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutViewSet.as_view({'post': 'logout'}), name='logout'),
    path('api/auth/user/info/', UserViewSet.as_view({'get': 'profile'}), name='user-info'),
    path('api/auth/change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
    # 为前端资源添加专门的静态文件路由
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.STATIC_ROOT, 'dist', 'assets')}),
    re_path(r'^vite.svg$', serve, {'document_root': os.path.join(settings.STATIC_ROOT, 'dist'), 'path': 'vite.svg'}),
    # 静态文件服务
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    # 媒体文件服务
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # 提供前端index.html
    path('', index, name='index'),
    # 处理所有其他路径，返回index.html以支持前端路由
    re_path(r'^(?!/api/).*$', index),
]