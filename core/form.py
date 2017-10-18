from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
import datetime


class LogInForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label="username",
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True)

    class Meta:
        model = User
        fields = ['username', 'password']