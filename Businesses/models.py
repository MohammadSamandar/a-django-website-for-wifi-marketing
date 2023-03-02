from django.db import models
from django.conf import settings
from login_signup.models import BusinessOwner
# Create your models here.




class Business(models.Model):

    name = models.CharField(max_length=100, unique=True)


    business_owner = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, related_name='my_business', null=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True)
    address = models.TextField(null=True)
    # router_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'کسب و کار'
        verbose_name_plural = 'کسب و کارها'

    def __str__(self):
        return str(self.name)






