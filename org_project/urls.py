"""org_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import routers

from organizations.backends import invitation_backend

from org_permissions.views import OrganizationUserViewSet, OrganizationPermissionViewSet

from .views import (
    main, LoginView, SignupView, logout_view, user_permissions,
    add_user_to_admins, add_user_to_members, remove_user_from_admins, remove_user_from_members
)


router = routers.DefaultRouter()
router.register(r'organizationuser', OrganizationUserViewSet, 'organization_users')
router.register(r'organizationpermission', OrganizationPermissionViewSet, 'organization_permissions')


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('organizations.urls')),
    re_path(r'^invitations/', include(invitation_backend().get_urls())),
    path('', main, name='main'),
    path('api/', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('user-permissions/', user_permissions, name='user_permissions'),
    path('add-user-to-admins/', add_user_to_admins, name='add_user_to_admins'),
    path('add-user-to-members/', add_user_to_members, name='add_user_to_members'),
    path('remove-user-from-admins/', remove_user_from_admins, name='remove_user_from_admins'),
    path('remove-user-from-members/', remove_user_from_members, name='remove_user_from_members'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
