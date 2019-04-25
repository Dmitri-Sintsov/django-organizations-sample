from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


def UniqueEmailValidator(value):
    user = User.objects.filter(email__iexact=value.strip()).first()
    if user is not None:
        raise ValidationError('The user with such email address already exists.')


def UniqueUsernameValidator(value):
    user = User.objects.filter(username__iexact=value.strip()).first()
    if user is not None:
        raise ValidationError('The user with such username already exists.')


class SignupForm(forms.Form):

    organization_name = forms.CharField(
        label="Company name",
        required=True,
    )
    first_name = forms.CharField(
        label="First name",
        required=True,
    )
    last_name = forms.CharField(
        label="Last name",
        required=True,
    )
    email = forms.CharField(
        widget=forms.EmailInput(),
        validators=[UniqueEmailValidator],
        label="Work email",
        required=True,
        max_length=75
    )
    username = UsernameField(
        validators=[UniqueUsernameValidator],
        label="User name",
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validate_password],
        strip=False,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm password",
        required=True
    )

    def clean(self):
        super().clean()
        if 'email' in self.cleaned_data:
            self.cleaned_data['email'] = self.cleaned_data['email'].strip()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self.add_error('password', 'Passwords does not match')
        return self.cleaned_data
