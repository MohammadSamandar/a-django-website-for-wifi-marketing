from django.contrib import admin
from .models import Ticket

# Register your models here.


# class TicketAdmin(admin.ModelAdmin):
#   date_hierarchy = 'created_at'
#   list_filter = ('status', 'assignee')
#   list_display = ('id', 'title', 'status', 'assignee', 'description', 'updated_at')
#   search_fields = ['title','status']
#
#
# admin.site.register(Ticket, TicketAdmin)


from django.contrib import admin
from .models import Ticket, FollowUp, Attachment


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description',
                    'assigned_to',
                    'created',
                    'updated',)


# Register Models
admin.site.register(Ticket, TicketAdmin)
admin.site.register(FollowUp)
admin.site.register(Attachment)