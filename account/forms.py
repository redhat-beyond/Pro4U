from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from account.models.profile import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Phone number already exists')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if User.objects.filter(first_name=first_name).exists():
            raise forms.ValidationError('This field is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if User.objects.filter(last_name=last_name).exists():
            raise forms.ValidationError('This field is required.')
        return last_name

