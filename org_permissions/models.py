from django.db import models
from django.contrib.auth.models import Permission

from organizations.models import Organization


class OrganizationPermissionManager(models.Manager):

    def add_user(self, organization_name, user):
        org, created = Organization.objects.get_or_create(name=organization_name)
        # We will assign organization admin / owner manually in Django Admin.
        org.add_user(user, is_admin=False)
        return org, created


class OrganizationPermission(models.Model):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, null=False, primary_key=True, verbose_name='Organization'
    )
    # One Organization to many Permission.
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name='organizations', verbose_name='Permission'
    )

    objects = OrganizationPermissionManager()

    class Meta:
        unique_together = ['organization', 'permission']
        verbose_name = 'Organization permission'
        verbose_name_plural = 'Organization permissions'

    def __str__(self):
        return '{} : {}'.format(str(self.organization), str(self.permission))
