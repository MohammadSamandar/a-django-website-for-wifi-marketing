from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from product_module.models import SubscriptionPlan
from django.contrib.auth.decorators import login_required
from .models import Order, OrderDetail

# Create your views here.

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
    context = {
        'order': current_order,
    }
    return render(request, 'business_owner_panel/user_basket.html', context)
