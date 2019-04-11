from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib.auth import views as auth_views

from .forms import SignupForm


class SignupView(FormView):

    form_class = SignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = User.objects.filter(email__iexact=form.cleaned_data['email']).first()
        organization_name = form.cleaned_data.pop('organization_name')
        del form.cleaned_data['confirm_password']
        if user is None:
            user = User.objects.create_user(
                **form.cleaned_data
            )
            user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:index')


class LoginView(auth_views.LoginView):

    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:index')
