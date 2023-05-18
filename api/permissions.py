from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import ValidationError
from loguru import logger
from titles.models import Review

logger.add('debug.json', format="{time} {level} {message}",
           level="DEBUG", rotation="1 week", compression="zip",
           serialize=True)


class AllowedUserFieldsForOwner(BasePermission):
    message = "You can`t change roles"

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.data.get('role') or request.data.get('email'):
            return False
        return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.author == request.user)


class OnlyOneReviewPerUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            user = request.user
            title_id = view.kwargs.get('title_id')
            if Review.objects.filter(author=user, title=title_id).exists():
                raise ValidationError('You can only leave one review per title')
        return True

