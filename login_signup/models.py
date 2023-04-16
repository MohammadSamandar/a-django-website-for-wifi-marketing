from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import SiteUser


# Create your models here.






class BusinessOwner(SiteUser):

    email_active_code = models.CharField(max_length=100, verbose_name='کد فعال سازی ایمیل', editable=False)
    avatar = models.ImageField(verbose_name='تصویر آواتار', null=True, blank=True)


    class Meta:
        verbose_name= 'صاحب کسب وکار'
        verbose_name_plural = 'صاحبان کسب و کار'



    def __str__(self):
        return self.username



# class Department(models.Model):
#     Name = models.CharField(verbose_name="Bölüm", max_length=11)
#     depadmin = models.ManyToManyField(BusinessOwner)
#     def __unicode__(self):
#         return self.name
