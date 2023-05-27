from django.urls import path
from . import views


urlpatterns = [

    path('', views.subscription_plan, name = 'subscription_plan'),
    path('<slug:slug>', views.subscription_plan_detial, name = 'subscription_plan_detail'),

]

