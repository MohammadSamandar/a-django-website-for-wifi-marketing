from django.shortcuts import render, redirect
from .models import BusinessCustomer
from .forms import RegisterForm
from . import helper
from django.contrib import messages
from Businesses.models import Business



def register_view(request):
    form = RegisterForm
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = BusinessCustomer.objects.filter(mobile__iexact=mobile).exists()

                if user:
                    user = BusinessCustomer.objects.filter(mobile__iexact=mobile, is_active=True).exists()
                    if user:
                        return redirect("http://shandiz.smartasha.ir/blogin.html")
                    else:
                        otp = helper.get_random_otp()
                        helper.send_otp(mobile, otp)
                        print(otp)

                        # user = BusinessCustomer(mobile=mobile, username=mobile, is_business_customer=True, otp=otp,
                        #                         is_active=False)
                        # shandiz = Business.objects.filter(name__iexact='شاندیز گالریا')
                        # user.business.set(shandiz)

                        request.session['user_mobile'] = mobile
                        request.session['otp'] = otp
                        return redirect('verify')
                else:

                    # send otp
                    otp = helper.get_random_otp()
                    helper.send_otp(mobile, otp)
                    print(otp)

                    # user = BusinessCustomer(mobile=mobile, username=mobile, is_business_customer=True, otp=otp,
                    #                         is_active=False)

                    # user.save()

                    # b = Business.objects.get(business_owner_id=request.user.id)
                    # customers = BusinessCustomer.objects.filter(business=b)

                    # shandiz = Business.objects.filter(name__iexact='شاندیز گالریا')
                    # user.business.set(shandiz)
                    request.session['user_mobile'] = mobile
                    request.session['otp'] = otp
                    # return HttpResponseRedirect(reverse('verify')) # this code not wotk in production
                    return redirect('verify')

        except BusinessCustomer.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                # helper.send_otp(mobile, otp)
                helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                # return HttpResponseRedirect(reverse('verify'))
                return redirect('verify')
    return render(request, 'customer_login/register_1_new_style.html', {'form': form})

def verify(request):


    try:
        mobile = request.session.get('user_mobile')
        otp = request.session.get('otp')
        user = BusinessCustomer(mobile=mobile, username=mobile, is_business_customer=True, otp=otp,
                                is_active=False)

        if request.method == "POST":

            if user:


                # check otp expiration
                # if not helper.check_otp_expiration(user.mobile):
                #     messages.error(request, "زمان وارد کردن کد تایید به اتمام رسید، دوباره امتحان کنید.")
                #     return redirect('register_page_customer')

                # if user.otp != int(request.POST.get('otp')):
                #     messages.error(request, "کد تایید اشتباه است!")
                #     return redirect('verify')

                user.is_active = True

                shandiz = Business.objects.get(name__iexact='شاندیز گالریا')
                user.business = shandiz
                user.save()


                # user.business.set(shandiz)


                return redirect("http://shandiz.smartasha.ir/blogin.html")




            if not helper.check_otp_expiration(user.mobile):
                messages.error(request, "زمان وارد کردن کد تایید به اتمام رسید، دوباره امتحان کنید.")
                return redirect('register_page_customer')

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "کد تایید اشتباه است!")
                return redirect('verify')

            user.is_active = True
            # user.save()
            shandiz = Business.objects.filter(name__iexact='شاندیز گالریا')
            user.business = shandiz
            user.save()
            # login(request, user)
            # return HttpResponseRedirect(reverse('alogin'))
            return redirect("http://shandiz.smartasha.ir/blogin.html")
        return render(request, 'customer_login/verify_1_new_style.html', {'mobile': mobile})

    except BusinessCustomer.DoesNotExist:
        messages.error(request, "خطایی رخ داد، دوباره امتحان کنید.")
        return redirect('register_page_customer')









def dashboard(request):

    return render(request, 'customer_login/alogin.html')


def vip_login(request):

    return redirect("http://shandiz.smartasha.ir/vip-login.html")
