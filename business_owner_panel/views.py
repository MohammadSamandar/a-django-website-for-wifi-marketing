from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.contrib import messages

from django.views import View
from django.views.generic import TemplateView
from tablib import Dataset

from django.http import HttpResponse
from .resources import CustomerResource
from Businesses.models import Business
# from site_module.models import Site_Setting
from .forms import UserProfileForm, ChangePasswordForm, CustomerForm
from login_signup.models import BusinessOwner
from customer_login.models import BusinessCustomer
from users.models import SiteUser
from django.contrib.auth import logout
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'business_owner_panel/dashboard.html'

@method_decorator(login_required, name='dispatch')
class EditUserProfile(View):
    def get(self, request: HttpRequest):
        current_user = BusinessOwner.objects.filter(id=request.user.id).first()


        user_profile_form = UserProfileForm(instance=current_user)
        context = {
            'form': user_profile_form,
            'current_user': current_user
        }
        return  render(request, 'business_owner_panel/edit_profile.html', context)


    def post(self, request: HttpRequest):
        current_user = BusinessOwner.objects.filter(id=request.user.id).first()
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=current_user)
        user_profile_form.save()

        if user_profile_form.is_valid():
            user_profile_form.save(commit=True)


        context = {
            'form' : user_profile_form,
            'current_user': current_user
        }

        return render(request, 'business_owner_panel/a/edit_profile.html', context)


@method_decorator(login_required, name='dispatch')
class ChangeUserPassword(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'business_owner_panel/change_password.html', context)

    def post(self, request: HttpRequest):

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: BusinessOwner = BusinessOwner.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')


        context = {
                'form': form
            }
        return render(request, 'business_owner_panel/a/change_password.html', context)



# View created for Customers list
@login_required
def CustomersPageView(request):
    # customers = BusinessCustomer.objects.all()
    # b = Business.objects.get(business_owner_id=request.user.id)
    b = BusinessOwner.objects.get(id=request.user.id)
    customers = BusinessCustomer.objects.filter(business=b)

    form = CustomerForm()
    if request.method == 'POST':

        form = CustomerForm(request.POST)
        if form.is_valid():
            user_mobile = form.cleaned_data.get('mobile')
            user: bool = BusinessCustomer.objects.filter(email__exact=user_mobile).exists()
            if user:
                form.add_error('mobile', 'مشتری با این موبایل قبلا ثبت شده است')
            else:

                new_user = BusinessCustomer(mobile=user_mobile, username=user_mobile)
                new_user.save()

                b = Business.objects.get(business_owner_id=request.user.id)
                new_user.business = b
                new_user.save()




                # form.save()

                return redirect('customers_list')

    context = {
        "customers": customers,
        'form': form,
    }
    return render(request, 'business_owner_panel/customers_list.html', context)




# View created for Update Customer page
@login_required
def UpdateCustomerPageView(request, customer_id):

    current_user = get_object_or_404(BusinessCustomer, pk=customer_id)

    form = CustomerForm(instance=current_user)
    # user_profile_form.save()

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()




            messages.success(request, "اطلاعات مشتری با موفقیت به روزرسانی شد! خدا خیر بده")
            return redirect('customers_list')


    context = {
        "form": form,
        'current_user': current_user
    }
    return render(request, 'business_owner_panel/update-customer.html', context)


# View created for Delete Customer page
@login_required
def DeleteCustomerPageView(request, customer_id):
    customer = BusinessCustomer.objects.get(id=customer_id)
    customer.delete()
    messages.error(request, "مشتری با موفقیت حذف شد! بر روح پاکش صلوات")
    return redirect('customers_list')







@login_required
def customers_records(request):
    return render(request, 'business_owner_panel/customers_records.html')

@login_required
def customers_export(request):
    person_resource = CustomerResource(request.user)

    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xlsx"'
    return response

@login_required
def customers_import(request):

    if request.method == 'POST':
        person_resource = CustomerResource(request.user)
        dataset = Dataset()
        new_persons = request.FILES['importData']
        if not new_persons.name.endswith('xlsx'):
            messages.info(request, 'فرمت فایل اشتباهه! حواست کجاست')
            return render(request, 'business_owner_panel/customers_import.html')

        imported_data = dataset.load(new_persons.read(), format='xlsx')
        for data in imported_data:

            try:
                user_exist_or_not = BusinessCustomer.objects.get(username=data[0])
                messages.error(request, "کاربری با این شماره وجود دارد")
                # return redirect("some_error_page")



            except BusinessCustomer.DoesNotExist:

                b = BusinessOwner.objects.get(id=request.user.id)
                value = BusinessCustomer(mobile=data[0], username=data[0], is_business_customer=True, business=b)
                # value.business = b
                value.save()
            messages.success(request, "مشتریان با موفقیت اضافه شدند!")

    return render(request, 'business_owner_panel/customers_import.html')



@login_required
def payments(reqest):
    return render(reqest, 'business_owner_panel/payments.html')

@login_required
def sms(reqest):
    return render(reqest, 'business_owner_panel/sms.html')





def panel_header_component(request):
    return render(request, 'business_owner_panel/components_references/site_header_component.html')

def panel_sidebar_component(request):
    # setting = Site_Setting.objects.filter(is_main_Setting=True).first()
    context = {

    }
    return render(request,
                  'business_owner_panel/components_references/site_sidebar_component.html', context)


def panel_footer_component(request):
    # setting = Site_Setting.objects.filter(is_main_Setting=True).first()
    context = {

    }
    return render(request,
                  'business_owner_panel/components_references/site_footer_component.html', context)

