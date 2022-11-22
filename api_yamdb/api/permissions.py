from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение для админов."""

    def has_permission(self, request, view):
        """Проверка , что пользователь авторизован
           и он админ или суперпользователь."""
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение для произведений, жанров и категорий.
       Изменять данные может только админ.
       Читать данные могут все."""

    def has_permission(self, request, view):
        """Проверка метод запроса безопасен или
           пользователь админ или суперпользователь."""
        return (request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminOrModeratorOrOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение для отзывов и комментариев.
       Изменять данные может админ, модератор или автор.
       Читать данные могут все."""

    def has_object_permission(self, request, view, obj):
        """Проверка метод запроса безопасен или
           пользователь имеет подходящую роль."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )

    def has_permission(self, request, view):
        """Проверка метод запроса безопасен или
           пользователь авторизован."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated)
