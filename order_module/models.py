from django.db import models
from login_signup.models import BusinessOwner
from product_module.models import SubscriptionPlan
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE,verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده / نشده')
    payment_date = models.DateField(verbose_name='تاریخ پرداخت', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات '


class OrderDetail(models.Model):
    product = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name='محصول')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    final_price = models.IntegerField(verbose_name='قیمت نهایی تکی محصول', null=True, blank=True)
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبد های خرید'
