from django.contrib.auth.backends import ModelBackend
from .models import BusinessCustomer


class MobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs['mobile']
        try:
            user = BusinessCustomer.objects.get(mobile=mobile)
        except BusinessCustomer.DoesNotExist:
            pass
