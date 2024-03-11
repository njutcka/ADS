from rest_framework.permissions import BasePermission


class IsAdminOrAuthor(BasePermission):
    message = 'Несоответствие прав доступа.'

    def has_permission(self, request, view):
        """Проверка на авторизацию"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверка на владельца или админа"""
        if request.user.role == request.user.is_admin or request.user.is_superuser:
            return True
        return obj.author == request.user
