from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserSettings
from .serializers import UserSettingsSerializer


class UserSettingsViewSet(viewsets.ViewSet):
    """用户设置视图集"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSettingsSerializer
    
    def get_object(self):
        obj, created = UserSettings.objects.get_or_create(
            user=self.request.user
        )
        return obj
    
    def list(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = UserSettingsSerializer(obj)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_settings(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = UserSettingsSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
