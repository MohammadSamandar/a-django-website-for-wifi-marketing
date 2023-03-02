from django.utils import timezone
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.template import RequestContext

from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from login_signup.models import BusinessOwner
from .models import Ticket, Attachment, FollowUp

# Create your views here.



# def index(request):
#
#     tickets = Ticket.objects.order_by('-created_at')[:5]
#     return render(request,'ticket/all-ticket.html', {'tickets': tickets})
#
# def ticket_by_id(request, ticket_id):
#
#     ticket = Ticket.objects.get(pk=ticket_id)
#     return render(request, 'ticket/ticket_detail.html', {'ticket':ticket})




def inbox_view(request):

    users = BusinessOwner.objects.all()
    tickets_unassigned = Ticket.objects.all().exclude(assigned_to__in=users)
    tickets_assigned = Ticket.objects.filter(assigned_to__in=users)

    return render(request, 'ticket/inbox.html',{"tickets_assigned": tickets_assigned,"tickets_unassigned": tickets_unassigned, })


def my_tickets_view(request):

    tickets = Ticket.objects.filter(assigned_to=request.user) \
                    .exclude(status__exact="DONE")
    tickets_waiting = Ticket.objects.filter(waiting_for=request.user) \
                                    .filter(status__exact="WAITING")

    return render(request, 'ticket/my_tickets.html',{"tickets": tickets,"tickets_waiting": tickets_waiting})


def all_tickets_view(request):

    tickets_open = Ticket.objects.all().exclude(status__exact="DONE")

    return render(request, 'ticket/all-ticket.html',{"tickets": tickets_open, })


def archive_view(request):

    tickets_closed = Ticket.objects.filter(status__exact="DONE")

    return render(request, 'ticket/archive.html',{"tickets": tickets_closed, })


def usersettings_update_view(request):

    user = request.user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_user = forms.UserSettingsForm(request.POST)

        # check whether it's valid:
        if form_user.is_valid():

            # Save User model fields
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()

            # redirect to the index page
            return HttpResponseRedirect(request.GET.get('next', '/inbox/'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form_user = forms.UserSettingsForm(instance=user)

    return render(request, 'ticket/settings.html', {'form_user': form_user, })


def ticket_create_view(request):

    if request.POST:
        form = forms.TicketCreateForm(request.POST)

        if form.is_valid():

            obj = form.save()
            # set owner
            # obj.owner = request.user
            obj.status = "TODO"
            obj.save()



            return redirect('inbox')

    else:
        form = forms.TicketCreateForm()

    return render(request, 'ticket/ticket_edit.html', {'form': form, })


def ticket_edit_view(request, pk):

    data = Ticket.objects.get(id=pk)

    if request.POST:
        form = forms.TicketEditForm(request.POST, instance=data)
        if form.is_valid():

            # set field closed_date to now() if status changed to "DONE"
            if form.cleaned_data['status'] == "DONE":
                data.closed_date = timezone.now()

            form.save()

            return redirect('inbox')

    else:
        form = forms.TicketEditForm(instance=data)

    return render(request, 'ticket/ticket_edit.html', {'form': form, })


def ticket_detail_view(request, pk):

    ticket = Ticket.objects.get(id=pk)
    attachments = Attachment.objects.filter(ticket=ticket)
    followups = FollowUp.objects.filter(ticket=ticket)

    return render(request, 'ticket/ticket_detail.html', {'ticket': ticket,'attachments': attachments,'followups': followups, })


def followup_create_view(request):

    if request.POST:

        form = forms.FollowupForm(request.POST)

        if form.is_valid():
            form.save()

            ticket = Ticket.objects.get(id=request.POST['ticket'])
            # mail notification to owner of ticket
            notification_subject = "[#" + str(ticket.id) + "] New followup"
            notification_body = "Hi,\n\n new followup created for ticket #" \
                                + str(ticket.id) \
                                + " (http://localhost:8000/ticket/" \
                                + str(ticket.id) \
                                + "/)\n\nTitle: " + form.data['title'] \
                                + "\n\n" + form.data['text']

            send_mail(notification_subject, notification_body, 'test@test.tld',
                      [ticket.owner.email], fail_silently=False)

            return redirect('inbox')

    else:
        form = forms.FollowupForm(initial={'ticket': request.GET.get('ticket'),
                                     'user': request.user})

    return render(request,'ticket/followup_edit.html',{'form': form, })


def followup_edit_view(request, pk):

    data = FollowUp.objects.get(id=pk)

    if request.POST:
        form = forms.FollowupForm(request.POST, instance=data)
        if form.is_valid():
            form.save()

            return redirect('inbox')

    else:
        form = forms.FollowupForm(instance=data)

    return render(request, 'ticket/followup_edit.html',{'form': form, })


def attachment_create_view(request):

    if request.POST:
        form = forms.AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            attachment = Attachment(
                ticket=Ticket.objects.get(id=request.GET['ticket']),
                file=request.FILES['file'],
                filename=request.FILES['file'].name,
                user=request.user
                # mime_type=form.file.get_content_type(),
                # size=len(form.file),
            )
            attachment.save()

            return redirect('inbox')

    else:
        form = forms.AttachmentForm()

    return render(request,'ticket/atachment_Add.html',{'form': form, })