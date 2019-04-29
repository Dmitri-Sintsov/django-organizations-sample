from django.db.models import Subquery, Value
from django.db.models.functions import Concat
from django.contrib.auth.backends import ModelBackend

from .models import OrganizationPermission


class OrganizationModelBackend(ModelBackend):

    perm_cache_name = '_organization_perm_cache'

    def get_organization_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if hasattr(user_obj, self.perm_cache_name):
            return getattr(user_obj, self.perm_cache_name)
        user_organizations = user_obj.organizations_organization.all()
        user_organizations_permissions = OrganizationPermission.objects.filter(
            organization__in=Subquery(user_organizations.values('pk'))
        )
        perms = user_organizations_permissions.annotate(
            perm=Concat('permissions__content_type__app_label', Value('.'), 'permissions__codename')
        ).values_list('perm', flat=True)
        setattr(user_obj, self.perm_cache_name, set(perms))
        return perms

    def has_perm(self, user_obj, perm, obj=None):
        if perm in self.get_organization_permissions(user_obj, obj):
            return True
        else:
            return super().has_perm(user_obj, perm, obj)
