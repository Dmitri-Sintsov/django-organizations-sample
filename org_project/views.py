from collections import OrderedDict

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.views.generic import FormView
from django.contrib.auth import logout, views as auth_views
from django.db.models import Value
from django.db.models.functions import Concat

from org_permissions.models import OrganizationPermission

from .forms import SignupForm


def main(request):
    return render(request, 'main.html')


class SignupView(FormView):

    form_class = SignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        organization_name = form.cleaned_data.pop('organization_name')
        del form.cleaned_data['confirm_password']
        user = User.objects.create_user(
            **form.cleaned_data
        )
        user.save()
        org, created = OrganizationPermission.objects.add_user(organization_name, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main')


class LoginView(auth_views.LoginView):

    template_name = 'login.html'

    def get_success_url(self):
        return reverse('main')


def logout_view(request):
    logout(request)
    return redirect('main')


def get_admin_url(model, action='change'):
    return reverse(
        "admin:{0}_{1}_{2}".format(
            model._meta.app_label,
            model._meta.model_name,
            action
        ), args=(model.pk,)
    )


def user_permissions(request):
    context_data = {
        'user_perms': OrderedDict([
            (perm, request.user.has_perm(perm)) for perm in Permission.objects.annotate(
                perm=Concat('content_type__app_label', Value('.'), 'codename')
            ).values_list('perm', flat=True)
        ]),
        'url_change_user': get_admin_url(request.user),
        'url_organization_user': reverse('admin:organizations_organizationuser_changelist'),
        'url_group_permission': reverse('admin:auth_group_changelist'),
        'url_organization_permission': reverse('admin:org_permissions_organizationpermission_changelist'),
    }
    return render(request, 'user_permissions.html', context_data)
