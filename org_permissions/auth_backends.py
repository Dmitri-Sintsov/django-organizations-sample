from django.contrib.auth.backends import ModelBackend

from organizations.models import Organization

from .models import OrganizationPermission


class OrganizationModelBackend(ModelBackend):

    def get_organization_permissions(self, user_obj, obj=None):
        return []

    def has_perm(self, user_obj, perm, obj=None):
        model_has_perm = super().has_perm(user_obj, perm, obj)
        if model_has_perm:
            return perm in self.get_organization_permissions(user_obj, obj)
        else:
            return False
