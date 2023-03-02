from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.register_view, name='register_page_customer'),
    path('verify/', views.verify, name='verify'),
    # path('login/', views.mobile_login, name='mobile_login'),
    path('alogin/', views.dashboard, name='alogin'),
    path('vip-login/', views.vip_login, name='vip_login'),
]
