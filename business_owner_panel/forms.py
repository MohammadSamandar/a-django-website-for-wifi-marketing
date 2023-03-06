from django import  forms
from django.core import validators
from django.core.exceptions import ValidationError

from login_signup.models import BusinessOwner
from customer_login.models import BusinessCustomer


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = BusinessOwner

        fields = ['username', 'first_name', 'last_name', 'mobile', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid',

            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid mb-3 mb-lg-0',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid mb-3 mb-lg-0',
                'placeholder': 'نام خانوادگی'
            }),

            'mobile': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg form-control-solid'
            }),


        }

        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'mobile': 'موبایل',
            'email': 'ایمیل',


        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-lg form-control-solid'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )


    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-lg form-control-solid'}),
        validators=[
            validators.MaxLengthValidator(100),
        ],

    )


    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-lg form-control-solid'}),
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')


        if password == confirm_password:
            return confirm_password


        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')




# Form created for Customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = BusinessCustomer
        fields = ['mobile', 'username']
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "form-control form-control-solid", }),
            "username": forms.TextInput(attrs={"class": "form-control form-control-solid", }),
            "is_active": forms.RadioSelect(attrs={"class": "form-control form-control-solid", }),

        }
        labels = {
            'mobile': 'mobile',
            'email': 'email',
            'is_active': 'is_active',

        }