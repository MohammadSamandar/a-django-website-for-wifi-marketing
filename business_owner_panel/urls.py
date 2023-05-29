from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name = 'user_panel_dashboard'),
    path('edit-profile/', views.EditUserProfile.as_view(), name = 'edit_profile'),
    path('change-password/', views.ChangeUserPassword.as_view(), name = 'chnage_password'),



    path('customers/', views.CustomersPageView, name="customers_list"),
    # path('add_customer/', views.AddCustomerPageView, name="add_customer"),
    path('update_customer/<str:customer_id>/', views.UpdateCustomerPageView, name="update_customer"),
    path('delete_customer/<str:customer_id>/', views.DeleteCustomerPageView, name="delete_customer"),

    path('customers-records/', views.customers_records, name = 'customers_records'),
    path('customers-export/', views.customers_export, name = 'customers_export'),
    path('customers-import/', views.customers_import, name = 'customers_import'),


    path('payments/', views.payments, name = 'payments'),
    path('subscription-plan/', views.subscription_plan, name = 'subscription_plan'),
    path('<slug:slug>', views.subscription_plan_detial, name = 'subscription_plan_detail'),

    path('order/', views.subscription_plan_detial, name = 'subscription_plan_detail'),
    path('sms/', views.sms, name = 'sms'),

]

