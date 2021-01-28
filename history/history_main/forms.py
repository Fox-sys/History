from django import forms
from .models import SolderPost, MainUser
from django.contrib.auth.forms import UserCreationForm


class SolderForm(forms.ModelForm):
    """
    Solder Model form
    """
    class Meta:
        model = SolderPost
        fields = ['first_name', 'middle_name', 'last_name', 'desc', 'is_alive', 'photo', 'birth_date', 'death_date']


class SignUpForm(UserCreationForm):
    """
    User sign up form
    """
    class Meta:
        model = MainUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        extra_fields = "death_date"
