from time import time

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse

from product_module.models import SubscriptionPlan
from django.contrib.auth.decorators import login_required
from .models import Order, OrderDetail
from django.template.loader import render_to_string


from django.conf import settings
import requests
import json

# Create your views here.



#? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

MERCHANT = 'd7c27d93-4761-4ed0-b55e-fb89a5a6af15'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/dashboard/order/verify-payment/'











@login_required
def add_product_to_order(request):
    product_id = request.GET.get('product_id')

    if request.user.is_authenticated:
        product = SubscriptionPlan.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            # get current user open order
            current_order, created= Order.objects.get_or_create(is_paid=False, user_id=request.user.id) # سبد خرید کاربر
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not  None:
                current_order_detail.save()
            else:
                new_order_dtail = OrderDetail(order_id=current_order.id, product_id=product_id)
                new_order_dtail.save()


            # add product to order

            return JsonResponse({
                'status': 'success',
                'message': 'محصول با موفقیت به سبد خرید اضافه شد.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'محصول معتبر نیست.'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'message': 'کاربر وارد نشده است.'
        })

@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'business_owner_panel/user_basket.html', context)


@login_required
def remove_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })


    # current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    # detail = current_order.orderdetail_set.filter(id=detail_id).first()

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if deleted_count is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    # detail.delete()

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    context = {
        'order': current_order,
    }
    data = render_to_string('business_owner_panel/user_basket_content.html', context)
    return JsonResponse({
        'status': 'success',
        'body': data
    })



@login_required
def request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)  # سبد خرید کاربر
    total_price = current_order.calculate_total_price()

    if total_price == 0:
        return redirect(reverse('user_basket'))

    data = {
        "MerchantID": MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }

    data["Amount"] = float(total_price * 10)
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


@login_required
def verify_payment(request: HttpRequest):

    authority = request.GET['Authority']

    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)  # سبد خرید کاربر
    total_price = current_order.calculate_total_price()

    if request.GET.get('Status') == 'OK':

        data = {
        "MerchantID": MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
        data["Amount"] = float(total_price * 10)
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()

                RefID = response['RefID']
                return render(request, 'business_owner_panel/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {str(RefID)} با موفقیت انجام شد'
                })
                # return HttpResponse({'status': True, 'RefID': response['RefID']})
            else:
                status = response['Status']
                return render(request, 'business_owner_panel/payment_result.html', {
                    'error': f'تراکنش شما با کد پیگیری {str(status)} با موفقیت انجام شد'
                })
                # return HttpResponse({'status': False, 'code': str(response['Status'])})
        return HttpResponse(response)

    else:
        return render(request, 'business_owner_panel/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })

