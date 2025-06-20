from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    agree_terms = forms.BooleanField(
        required=True,
        label='Я принимаю <a href="/terms/" target="_blank">условия использования</a> и <a href="/privacy/" target="_blank">политику конфиденциальности</a>',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'agree_terms')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_place', 'death_place', 'latitude', 'longitude', 'photo', 'media_archive'] 