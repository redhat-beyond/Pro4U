from django import forms
from django.contrib.auth.models import User
from account.models.profile import Profile
from account.models.professional import Professional


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    country = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    address = forms.CharField(max_length=30)

    class Meta:
        model = Profile
        fields = ['phone_number', 'country', 'city', 'address']


class ProfessionalUpdateForm(forms.ModelForm):
    description = forms.CharField(max_length=500)

    class Meta:
        model = Professional
        fields = ['description']
