from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from product_module.models import SubscriptionPlan

# Create your views here.



@login_required
def subscription_plan(request):

    plans = SubscriptionPlan.objects.all().order_by('duration')

    context = {
        'plans': plans,
    }


    return render(request, 'business_owner_panel/subscriptionplan.html', context)


@login_required
def subscription_plan_detial(request, slug):

    plans = get_object_or_404(SubscriptionPlan, slug=slug)

    context = {
        'plans': plans,
    }


    return render(request, 'business_owner_panel/subscriptionplan_detail.html', context)
