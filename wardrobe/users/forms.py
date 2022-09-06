from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator(allowlist=['uwr.edu.pl'])])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
