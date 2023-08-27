import random
import string
from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.conf import settings
from django.core.mail import send_mail
from accounts.models import User

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def send_mail_task(message,subj,email):
    subject=subj
    message=message
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject,message,from_email,[str(email),],fail_silently=True)


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'user_type',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UmujyanamaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name','email','phone_number','identification_number')