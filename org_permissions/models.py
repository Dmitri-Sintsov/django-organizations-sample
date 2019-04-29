from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import Permission

from organizations.models import Organization


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


class OrganizationPermissionManager(models.Manager):

    def add_user(self, organization_name, user):
        org, created = Organization.objects.get_or_create(name=organization_name)
        # We will assign organization admin / owner manually in Django Admin.
        org.add_user(user, is_admin=False)
        return org, created

    def setup_organizations(self, permissions=None):
        if permissions is None:
            permissions = DEFAULT_ORGANIZATION_PERMISSIONS
        organizations_dict = {}
        for organization_name, perm_list in permissions.items():
            organization, created = Organization.objects.get_or_create(name=organization_name)
            for perm in perm_list:
                app_label, codename = perm.split('.')
                permission = Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()
                if permission is None:
                    raise ValidationError('No such permission: %s', params=[perm])
                organization_permission, created = OrganizationPermission.objects.get_or_create(organization=organization)
                organization_permission.permissions.add(permission)
            organizations_dict[organization_name] = organization
        return organizations_dict


class OrganizationPermission(models.Model):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name='org_perm', null=False, primary_key=True, verbose_name='Organization'
    )
    # Many Permission to many OrganizationPermission.
    permissions = models.ManyToManyField(
        Permission, verbose_name='Permissions'
    )

    objects = OrganizationPermissionManager()

    class Meta:
        verbose_name = 'Organization permission'
        verbose_name_plural = 'Organization permissions'

    def __str__(self):
        return '{} : {}'.format(str(self.organization), ' : '.join(str(perm) for perm in self.permissions.all()))
