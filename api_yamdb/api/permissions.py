from rest_framework import permissions


class IfUserIsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IfUserIsModerator(permissions.BasePermission):
    message = 'Действие разрешено только модератору!'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'moderator' or request.user.is_superuser
        return False


class IfUserIsAdministrator(permissions.BasePermission):
    message = 'Действие разрешено только администратору!'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        return False


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )
