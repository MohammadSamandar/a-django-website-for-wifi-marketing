from django.urls import path
from . import views


urlpatterns = [

    path('add-to-order', views.add_product_to_order, name='add_product_to_order'),
    path('user-basket/', views.user_basket, name= 'user_basket'),
    path('remove-basket-detail/', views.remove_order_detail, name= 'remove_order_detail_ajax'),

]

