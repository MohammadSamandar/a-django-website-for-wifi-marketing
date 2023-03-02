from django import forms
from . import models


class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.BusinessCustomer
        fields = ['mobile', ]
