
from .models import Document
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib import messages

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


 

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'username-field',
                'class': 'form-control form-control-placeholder ',
                'placeholder': 'Username'
            }
        ),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password-field',
                'class': 'form-control form-control-placeholder',
                'placeholder': 'Password'
            }
        ),
        label=''
    )
