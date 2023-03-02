from django.db import models
from django.contrib.auth.models import AbstractUser
from Businesses.models import Business
from customer_login.myusermanager import MyUserManager
from users.models import SiteUser




class BusinessCustomer(SiteUser):
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    business = models.ForeignKey(Business, related_name='customer', on_delete=models.CASCADE, null=True, blank=True)


    objects = MyUserManager()

    # username = None
    #
    # USERNAME_FIELD = 'mobile'
    #
    # REQUIRED_FIELDS = []


    backend = 'custom_login.mybackend.ModelBackend'

    class Meta:
        verbose_name= 'مشتری کسب و کار'
        verbose_name_plural = 'مشتریان کسب و کارها'



    def __str__(self):
        return str(self.mobile)












