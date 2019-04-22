from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib.auth import logout, views as auth_views

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
        return reverse('login')


class LoginView(auth_views.LoginView):

    template_name = 'login.html'

    def get_success_url(self):
        return reverse('login')


def logout_view(request):
    logout(request)
    return redirect('login')
