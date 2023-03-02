from django.contrib import admin
from .models import BusinessCustomer


# Register your models here.
class BusinessCustomer_Admin(admin.ModelAdmin):


    list_display = ('mobile', 'is_active')

    search_fields = ('mobile',)


admin.site.register(BusinessCustomer,BusinessCustomer_Admin)

