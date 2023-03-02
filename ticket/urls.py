from django.urls import path
from . import views


# urlpatterns = [
#     path('', views.index, name='index_ticket'),
#     path('<int:ticket_id>', views.ticket_by_id, name='detail_of_ticket')
# ]


urlpatterns = [


    # Login and settings pages



    # create new ticket
    path(r'new/', views.ticket_create_view, name='ticket_new'),

    # edit ticket
    path(r'edit/(<pk>)/', views.ticket_edit_view, name='ticket_edit'),

    # view ticket
    path(r'detail/(<pk>)/', views.ticket_detail_view, name='ticket_detail'),

    # create new followup
    path(r'followup/new/', views.followup_create_view, name='followup_new'),

    # edit followup
    path(r'followup/edit/(<pk>)/', views.followup_edit_view, name='followup_edit'),

    # create new attachment
    path(r'attachment/new/', views.attachment_create_view, name='attachment_new'),

    # ticket overviews
    path(r'inbox/', views.inbox_view, name='inbox'),

    path(r'my-tickets/', views.my_tickets_view, name='my-tickets'),

    path(r'', views.all_tickets_view, name='all-tickets'),

    path(r'archive/', views.archive_view, name='archive'),

]
