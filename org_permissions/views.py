from rest_framework import viewsets
from .permissions import ModelPermissions

from organizations.models import OrganizationUser

from .models import OrganizationPermission

from .serializers import OrganizationUserSerializer, OrganizationPermissionSerializer


class OrganizationUserViewSet(viewsets.ModelViewSet):

    # Sample of perms_map override.
    perms_map = {
        'POST': 'organizations.view_organizationuser',
    }

    permission_classes = [ModelPermissions]
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer


class OrganizationPermissionViewSet(viewsets.ModelViewSet):

    permission_classes = [ModelPermissions]
    queryset = OrganizationPermission.objects.all()
    serializer_class = OrganizationPermissionSerializer
