from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from login_signup.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import BusinessOwner
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from utils.email_service import send_email
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'login_signup/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user_mobile = register_form.cleaned_data.get('mobile')
            user: bool = BusinessOwner.objects.filter(email__iexact=user_email, username__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'کاربری با این ایمیل قبلا ثبت نام کرده است')
            else:
                new_user = BusinessOwner(email=user_email, email_active_code=get_random_string(72),
                                is_active=False, username=user_email, is_business_owner=True, mobile=user_mobile)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'email/active_accounts.html')
                messages.success(request, "ایمیل فعال سازی حساب کاربری برای شما ارسال شد. ایمیل خودرا چک نمایید")
                # return redirect(reverse('login_page'))




        context = {
                'register_form': register_form,

            }
        return render(request, 'login_signup/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):

        user: BusinessOwner = BusinessOwner.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None: # اگر کاربر وجود داره
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # show success message to user
                return redirect(reverse('login_page'))
            else:
                # show "your account was activated" message to user
                pass

        raise Http404


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'login_signup/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: BusinessOwner = BusinessOwner.objects.filter(email__iexact=user_email).first()

            if user is not None: # اگر کاربر وجود داره
                if not user.is_active: # اگر حساب کاربری فعال نیست
                     # show error
                     login_form.add_error('email', 'حساب کاربری شما فعال نشده است')

                else:
                    is_password_correct = user.check_password(user_password) # مقایسه پسورد وارد شده در فرم و پسورد موجود در دیتابیس
                    if is_password_correct: # اگر پسورد درست بود یا در دیتابیس موجود بود
                        login(request, user) # لاگین انجام بشود
                        return redirect(reverse('user_panel_dashboard')) # بعد از لاگین به این صفحه ریدایرکت بشود
                    else: # اگر پسورد وارد شده درست نبود
                        login_form.add_error('email', 'نام کاربری و یا کلمه عبور اشتباه است')

            else: # اگر کاربر وجود نداره
                login_form.add_error('email', 'نام کاربری و یا کلمه عبور اشتباه است')


        context = {
            'login_form': login_form
        }
        # اگر فرم valid نیست این صفحه را برگردان
        return render(request, 'login_signup/login.html', context)



class ForgetPassword(View):

    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'login_signup/forgot_password.html', context)


    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: BusinessOwner = BusinessOwner.objects.filter(email__iexact=user_email).first()

            if user is not None: # اگه یوزری وجود داشت
                # ارسال ایمیل به یوزری که در دیتابیس وجود دارد
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'email/forgot_password.html')
                return redirect(reverse('login_page'))


        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'login_signup/forgot_password.html', context)



class ResetPassword(View):

    def get(self, request: HttpRequest, active_code):

        user: BusinessOwner = BusinessOwner.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))


        reset_pass_form = ResetPasswordForm()
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'login_signup/reset_password.html', context)


    def post(self, request: HttpRequest, active_code):

        reset_pass_form = ResetPasswordForm(request.POST)
        user: BusinessOwner = BusinessOwner.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_password = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))




        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'login_signup/reset_password.html', context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


