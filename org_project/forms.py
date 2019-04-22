from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User, Permission
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


class PermissionForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ['codename']
        widgets = {
            'codename': forms.Select(choices=Permission.objects.values_list('pk', 'codename'))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def set_user(self, user=None):
        self.user = user

    def get_codename_value(self):
        return dict(self.fields['codename'].widget.choices).get(int(self.cleaned_data['codename']))

    def clean(self):
        super().clean()
        codename = self.get_codename_value()
        if self.user is None:
            self.add_error('codename', 'Please specify user to check the permissions')
        elif not self.user.has_perm(codename):
            self.add_error('codename', format_html(
                'User "{}" has no permission "{}"', self.user, codename
            ))
