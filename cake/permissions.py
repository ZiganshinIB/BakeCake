from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Кастомная разрешения только для владельца объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user

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

class CanCreateCakeLevel(BasePermission):
    """
    Проверка разрешения на создание уровня торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.add_cakelevl'):
            return True
        return False

class CanUpdateCakeLevel(BasePermission):
    """
    Проверка разрешения на обновление уровня торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_cakelevl'):
            return True
        return False


class CanDeleteCakeLevel(BasePermission):
    """
    Проверка разрешения на удаление уровня торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_cakelevl'):
            return True
        return False


class CanCreateCakeShape(BasePermission):
    """
    Проверка разрешения на создание формы торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.add_cakeshape'):
            return True
        return False

class CanUpdateCakeShape(BasePermission):
    """
    Проверка разрешения на обновление формы торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_cakeshape'):
            return True
        return False


class CanDeleteCakeShape(BasePermission):
    """
    Проверка разрешения на удаление формы торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_cakeshape'):
            return True
        return False


class CanCreateCakeTopping(BasePermission):
    """
    Проверка разрешения на создание топпинга торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.add_caketopping'):
            return True
        return False


class CanUpdateCakeTopping(BasePermission):
    """
    Проверка разрешения на обновление топпинга торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_caketopping'):
            return True
        return False


class CanDeleteCakeTopping(BasePermission):
    """
    Проверка разрешения на удаление топпинга торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_caketopping'):
            return True
        return False


class CanCreateCakeBerry(BasePermission):
    """
    Проверка разрешения на создание ягод торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.add_cakeberry'):
            return True
        return False


class  CanUpdateCakeBerry(BasePermission):
    """
    Проверка разрешения на обновление ягод торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_cakeberry'):
            return True
        return False


class CanDeleteCakeBerry(BasePermission):
    """
    Проверка разрешения на удаление ягод торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_cakeberry'):
            return True
        return False

class CanCreateCakeDecor(BasePermission):
    """
    Проверка разрешения на создание вкуса торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.add_cakedecor'):
            return True
        return False

class CanUpdateCakeDecor(BasePermission):
    """
    Проверка разрешения на обновление вкуса торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_cakedecor'):
            return True
        return False


class CanDeleteCakeDecor(BasePermission):
    """
    Проверка разрешения на удаление вкуса торта
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_cakedecor'):
            return True
        return False

class CanCreateOrder(BasePermission):
    """
    Проверка разрешения на создание заказа
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False


class CanUpdateOrder(BasePermission):
    """
    Проверка разрешения на обновление заказа
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.change_order'):
            return True
        return False


class CanDeleteOrder(BasePermission):
    """
    Проверка разрешения на удаление заказа
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.has_perm('cake.delete_order'):
            return True
        return False