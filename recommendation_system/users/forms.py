from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-user',
                   'placeholder': 'Password',
                   'label': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                          'placeholder': 'Repeat Password',
                                          'label': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'johnsmith1972'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'johnsmith@example.com', 'label': 'Email'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'johnsmith1972'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter your password'})
    )

    class Meta:
        fields = ['username', 'password']
