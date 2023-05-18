from django.db.models import Q
from softdelete.models import SoftDeleteManager


class SoftDeleteManagerForSlug(SoftDeleteManager):
    def get(self, *args, **kwargs):
        if 'slug' or 'pk' in kwargs:
            return self.all_with_deleted().get(*args, **kwargs)
        else:
            return self._get_self_queryset().get(*args, **kwargs)

    def create(self, **kwargs):
        name = kwargs.get('name')
        slug = kwargs.get('slug')

        # Check if a soft-deleted model with the same name exists
        soft_deleted_all = self._get_base_queryset().filter(deleted_at__isnull=False)
        same_name = self._get_base_queryset().filter(Q(name__iexact=name) | Q(slug__iexact=slug))
        soft_deleted = soft_deleted_all & same_name
        if soft_deleted:
            soft_deleted.first().delete()

        return super().create(**kwargs)
