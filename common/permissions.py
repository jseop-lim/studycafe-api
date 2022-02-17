from rest_framework import permissions


class AdminReadOnly(permissions.BasePermission):
    """
    관리자 계정으로 읽기만 가능
    """
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS and request.user and request.user.is_staff)


class IsOwner(permissions.BasePermission):
    """
    사용자 본인만 read/write 가능
    """
    def has_permission(self, request, view):
        return bool(request.user and view.kwargs['pk'] == request.user.id)