from django import forms
from django.core.validators import MinValueValidator


class TypeOfJobForm(forms.Form):
    typeOfJob_name = forms.CharField(max_length=120, required=True)
    price = forms.IntegerField(validators=[MinValueValidator(0)], required=True)
