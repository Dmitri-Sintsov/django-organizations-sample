from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.views.generic import FormView
from django.contrib.auth import logout, views as auth_views

from organizations.models import OrganizationUser

from org_group.models import GroupOrganization

from .forms import SignupForm


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
        group, created = Group.objects.get_or_create(name='"{}" group'.format(organization_name))
        group.user_set.add(user)
        org, created = GroupOrganization.objects.get_or_create(
            group=group,
            defaults={'name': organization_name}
        )
        # We will assign organization admin / owner manually in Django Admin.
        org.add_user(user, is_admin=False)
        # org.change_owner(org_user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class LoginView(auth_views.LoginView):

    template_name = 'main.html'

    def get_success_url(self):
        return reverse('login')


def logout_view(request):
    logout(request)
    return redirect('login')
