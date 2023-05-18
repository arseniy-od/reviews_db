from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError, MethodNotAllowed


class SearchMixin:
    queryset = None

    def get_queryset(self):
        search_queryset = self.search()
        if search_queryset:
            return search_queryset
        return self.queryset

    def search(self):
        search_query = self.request.query_params.get('search')
        if search_query:
            result = self.queryset.filter(name__icontains=search_query)
            return result


class GetDeletedObjectsMixin:
    def get_object(self):
        queryset = self.filter_queryset(self.model.objects.all_with_deleted())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        if self.request.method != 'POST' and obj.deleted_at:
            raise MethodNotAllowed(self.request.method)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class UserRoleMixin:
    def _check_role_and_save(self, serializer):
        role = self.request.data.get('role')

        if role not in ['user', 'moderator', 'admin', None]:
            raise ValidationError("Role has to be in [user, moderator, admin]")

        if role == 'moderator':
            serializer.save(is_staff=True)

        if role == 'admin':
            serializer.save(is_staff=True, is_superuser=True)

        serializer.save()

    def perform_update(self, serializer):
        self._check_role_and_save(serializer)

    def perform_create(self, serializer):
        self._check_role_and_save(serializer)
