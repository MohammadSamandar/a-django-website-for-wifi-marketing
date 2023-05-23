from django.contrib import admin
from . import models
# Register your models here.


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_filter = ['duration', 'price', 'is_active']
    list_display = ['title', 'price', 'duration', 'is_active']
    list_editable = ['is_active']


admin.site.register(models.SubscriptionPlan, SubscriptionPlanAdmin)