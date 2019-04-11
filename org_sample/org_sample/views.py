from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib.auth import views as auth_views

from organizations.utils import create_organization

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
        # We will assign organization admin manually in Django Admin.
        org = create_organization(user, organization_name, org_user_defaults={'is_admin': False})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class LoginView(auth_views.LoginView):

    template_name = 'main.html'

    def get_success_url(self):
        return reverse('login')
