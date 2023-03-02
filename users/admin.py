from django.contrib import admin
from .models import SiteUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class SiteUser_Admin(admin.ModelAdmin):

    list_display = ('username','is_business_customer', 'is_business_owner', 'email', 'mobile')
    search_fields = ('email','mobile')

admin.site.register(SiteUser, UserAdmin)
