
from django import forms
from django.contrib.auth.hashers import check_password
from home.models import *
from healthCenter.models import *
from accounts.models import ClinicAddress

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, min_length=3, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class HouseHoldForm(forms.ModelForm):
    phone_number=forms.CharField(max_length=13,min_length=13)
    mother_id_no=forms.CharField(max_length=16,min_length=16)
    father_id_no=forms.CharField(max_length=16,min_length=16)
    class Meta:
        model = HouseHold
        fields = ('father_full_name', 'father_id_no','mother_full_name','mother_id_no','number_child','phone_number','village')


class BirthChildForm(forms.ModelForm):
    class Meta:
        model = BirthChild
        fields = ('full_name','description','birth_date','village')
    
class BirthAssignForm(forms.ModelForm):
    class Meta:
        model = BirthChild
        fields=('vigirant',)

    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users', None)
        super().__init__(*args, **kwargs)
        self.fields["vigirant"].queryset =self.users

class PregnancyForm(forms.ModelForm):
    phone_number=forms.CharField(max_length=13,min_length=13)
    class Meta:
        model = Pregnancy
        fields = ('full_name','description','phone','birth_date','village','vigirant')

class PregnancyAssign(forms.ModelForm):

    class Meta:
        model = Pregnancy
        fields=('vigirant',)

    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users', None)
        super().__init__(*args, **kwargs)
        self.fields["vigirant"].queryset =self.users


class UserChangePassword(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('new_password', 're_password', 'password')

    def clean_password(self):
        if check_password(self.cleaned_data.get('password'), self.instance.password):

            if self.cleaned_data.get('new_password') == self.cleaned_data['re_password']:
                return self.cleaned_data.get('new_password')
            raise forms.ValidationError("Passwords don't match")
        raise forms.ValidationError("Use Correct password")

    def save(self, commit=False):
        # Save the provided password in hashed format
        user = super(UserChangePassword, self).save(commit=False)
        user.set_password(self.cleaned_data.get("new_password"))
        if commit:
            user.save()
        return user
    
class UserInfoPassword(forms.ModelForm):
    phone_number=forms.CharField(max_length=13,min_length=13)
    class Meta:
        model = User
        fields = ('full_name', 'phone_number')
        

class ClinicAddressForm(forms.ModelForm):
    class Meta:
        model = ClinicAddress
        fields = ('sector',)

class BookingForm(forms.ModelForm):
    phone_number=forms.CharField(max_length=13,min_length=13)
    class Meta:
        model = BookingMedical
        fields = ('full_name','phone_number','description','village')
    