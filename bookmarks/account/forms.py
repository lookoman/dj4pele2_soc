from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    # clean_<имя поля> - для проверки валидности и очистки этого поля
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_email(self):
        mail = self.cleaned_data['email']
        if User.objects.filter(email=mail).exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует.')
        return mail


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        mail = self.cleaned_data['email']
        qs = User.objects.filter(email=mail).exclude(id=self.instance.id)
        if qs.exists():
            raise forms.ValidationError('Пользователь с такой электронной почтой уже существует.')
        return mail


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
