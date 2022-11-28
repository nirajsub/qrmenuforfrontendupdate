from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Admin
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['category', 'todays_special', 'product_discount', 'product_newprice', 'exclusive']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user']

class SpecialForm(ModelForm):
    class Meta:
        model = Product
        fields = ['todays_special']
    
class ExclusiveForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_discount', 'product_newprice']