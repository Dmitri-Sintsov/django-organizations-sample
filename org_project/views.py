from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib.auth import logout, views as auth_views

from org_permissions.models import OrganizationPermission

from .forms import SignupForm, PermissionForm


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


class CheckUserPermissionsView(FormView):

    form_class = PermissionForm
    template_name = 'check_user_permissions.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.set_user(self.request.user)
        return form

    def get_initial(self):
        initial = super().get_initial()
        if 'codename' in self.request.POST:
            initial['codename'] = self.request.POST.get('codename')
        return initial

    def form_valid(self, form):
        codename_value = form.get_codename_value()
        return render(request=self.request, template_name=self.template_name, context={
            'form': form, 'codename_value': codename_value
        })
