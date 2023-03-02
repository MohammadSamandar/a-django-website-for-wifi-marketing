from import_export import resources
from django.http import HttpRequest
from customer_login.models import BusinessCustomer
from Businesses.models import Business


class CustomerResource(resources.ModelResource):

    def __init__(self, user):
        self.user = user

    def get_queryset(self):
        b = Business.objects.get(business_owner_id=self.user.id)
        return self._meta.model.objects.filter(business=b)

    class Meta:
        model = BusinessCustomer
        skip_unchanged = True
        report_skipped = False
        fields = ('mobile')