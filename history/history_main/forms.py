from django import forms
from .models import SolderPost, MainUser, BadWord
from django.contrib.auth.forms import UserCreationForm
from random import choice
from string import ascii_letters
import re

class SolderForm(forms.ModelForm):
    """
    Solder Model form
    """
    filter_fields = ['first_name', 'middle_name', 'last_name', 'desc']
    decode_fields = {'first_name': 'Имя', 'middle_name': 'Отчество', 'last_name': 'Фамилия', 'desc': 'Описание'}

    def black_list_validated(self):
        black_list = BadWord.objects.all()
        for field in self.filter_fields:
            for word in black_list:
                if not re.search(f'\d({word})\d', self.cleaned_data[field], re.M|re.I) is None:
                    return {self.decode_fields[field]: word}
        return None

    class Meta:
        model = SolderPost
        fields = ['first_name', 'middle_name', 'last_name', 'desc', 'is_alive', 'photo', 'birth_date', 'death_date']


class SignUpForm(UserCreationForm):
    """
    User sign up form
    """
    class Meta:
        model = MainUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'avatar')


class EditProfileForm(forms.ModelForm):
    """
    Form for editing profile
    """

    class Meta:
        model = MainUser
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'email_is_hidden', \
                  'phone', 'phone_is_hidden', 'avatar')


class ChangePasswordForm(forms.Form):
    user = forms.CharField()
    secret_key = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        user = MainUser.objects.get(username=self.cleaned_data["user"])
        password = self.check_password(user)
        if password:
            user.set_password(password)
            user.secret_key = ''.join(choice(ascii_letters) for i in range(20))
            user.save()
            return user
        return None


    def check_password(self, user):
        if len(self.cleaned_data['password2']) >= 8 and self.cleaned_data['password1'] == self.cleaned_data['password2'] and user.secret_key == self.cleaned_data['secret_key']:
            return self.cleaned_data['password2']
        return None


class GetUserForm(forms.Form):
    username = forms.CharField()

    def get_username(self):
        return self.cleaned_data["username"]