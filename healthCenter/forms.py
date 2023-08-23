
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, min_length=3, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

