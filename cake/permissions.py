from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Кастомная разрешения только для владельца объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.client == request.user

class CanUpdateCake(BasePermission):
    """
    Проверка разрешения на обновление торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_cake'):
            return True
        return False


class CanDeleteCake(BasePermission):
    """
    Проверка разрешения на удаление торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_cake'):
            return True
        return False