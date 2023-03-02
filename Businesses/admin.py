from django.contrib import admin
from .models import Business
# Register your models here.
class Business_Admin(admin.ModelAdmin):

    list_display = ('name', 'business_owner', 'phone_number',)
    search_fields = ('name', 'business_owner', 'phone_number')


admin.site.register(Business, Business_Admin)