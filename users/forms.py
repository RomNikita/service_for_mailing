from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6)




