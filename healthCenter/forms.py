
from django import forms
from home.models import HouseHold
from healthCenter.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, min_length=3, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class HouseHoldForm(forms.ModelForm):
    class Meta:
        model = HouseHold
        fields = ('father_full_name', 'father_id_no','mother_full_name','mother_id_no','number_child','phone_number','village')


class BirthChildForm(forms.ModelForm):
    class Meta:
        model = BirthChild
        fields = ('full_name','description','birth_date','village')

class PregnancyForm(forms.ModelForm):
    class Meta:
        model = Pregnancy
        fields = ('full_name','description','phone','birth_date','village')
