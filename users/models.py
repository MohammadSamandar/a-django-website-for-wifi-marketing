from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class SiteUser(AbstractUser):

    is_business_customer = models.BooleanField('business customer', default=False)
    is_business_owner = models.BooleanField('business owner', default=False)
    mobile = models.CharField(max_length=11, null=True)
    # username = None




    class Meta:
        verbose_name= 'کاربر'
        verbose_name_plural = 'همه کاربران'

