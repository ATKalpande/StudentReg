# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudForm(forms.Form):
    s_name = forms.CharField(max_length=30)
    s_class = forms.CharField(max_length=30)
    s_add = forms.CharField(max_length=30)
    s_email = forms.EmailField(max_length=30)

class  SForm(forms.Form):
    s_name =forms.CharField(max_length=30)
    
