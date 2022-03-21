from rest_framework import permissions


class IfUserIsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IfUserIsModerator(permissions.BasePermission):
    message = 'Действие разрешено только модератору!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'moderator'


class IfUserIsAdministrator(permissions.BasePermission):
    message = 'Действие разрешено только администратору!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_superuser
            or request.method in permissions.SAFE_METHODS
        )
