from rest_framework.permissions import DjangoModelPermissions


# Key is an Organization name, value is the list of Permission.
DEFAULT_ORGANIZATION_PERMISSIONS = {
    'Organization Admins': [
        'organizations.view_organizationuser',
        'organizations.add_organizationuser',
        'organizations.change_organizationuser',
        'organizations.delete_organizationuser',
        'org_permissions.view_organizationpermission',
        'org_permissions.add_organizationpermission',
        'org_permissions.change_organizationpermission',
        'org_permissions.delete_organizationpermission',
    ],
    'Organization Users': [
        'organizations.view_organizationuser',
        'org_permissions.view_organizationpermission',
    ],
}


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        if hasattr(view, 'perms_map') and request.method in view.perms_map:
            # Override default perms_map from view / ViewSet.
            perms = view.perms_map[request.method]
            if isinstance(perms, str):
                perms = [perms]
        else:
            queryset = self._queryset(view)
            perms = self.get_required_permissions(request.method, queryset.model)

        return request.user.has_perms(perms)
