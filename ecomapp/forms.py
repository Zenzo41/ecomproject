from django import forms
from .models import *
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by","shipping_address","mobile","email"]

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
    # Adding the missing fields
    full_name = forms.CharField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Customer
        fields = ["username", "password", "email", "full_name", "address"]

    #for unique username
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists"
            )
        return uname