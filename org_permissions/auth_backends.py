from django.db.models import Subquery
from django.contrib.auth.backends import ModelBackend

from .models import OrganizationPermission


class OrganizationModelBackend(ModelBackend):

    # Todo: add caching.
    def get_organization_permissions(self, user_obj, obj=None):
        user_organizations = user_obj.organizations_organization.all()
        user_organizations_permissions = OrganizationPermission.objects.filter(
            organization__in=Subquery(user_organizations.values('pk'))
        )
        return user_organizations_permissions.values_list('permission__codename', flat=True)

    def has_perm(self, user_obj, perm, obj=None):
        has_org_perm = perm in self.get_organization_permissions(user_obj, obj)
        if has_org_perm:
            return True
        else:
            return super().has_perm(user_obj, perm, obj)
