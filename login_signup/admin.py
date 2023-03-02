from django.contrib import admin
from .models import BusinessOwner, SiteUser
# Register your models here.

class BusinessOwner_Admin(admin.ModelAdmin):

    list_display = ('username', 'email', 'mobile')
    search_fields = ('email', 'username', 'mobile')





admin.site.register(BusinessOwner, BusinessOwner_Admin)


