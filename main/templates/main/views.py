from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView

from main.forms import MailingCreateForm, ClientCreateForm, MessageCreateForm
from main.models import Mailing, Client, Message, LogsOfMailing
from main.runapscheduler import scheduler, send_mailing


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/home.html'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'main/mailing_form.html'
    form_class = MailingCreateForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        response = super().form_valid(form)

        email_for_mail = self.object.client.email
        subject_of_mail = self.object.message.subject_of_letter
        body_of_message = self.object.message.body_of_letter

        subject = subject_of_mail
        message = body_of_message
        sender_email = 'noreplyskypro9@gmail.com'
        recipient_list = [email_for_mail]
        send_mail(subject, message, sender_email, recipient_list)

        return response


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:home')
    template_name = 'main/mailing_confirm_delete.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateForm
    success_url = reverse_lazy('main:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class ClientListView(ListView):
    model = Client


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm
    success_url = reverse_lazy('main:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class LogsOfMailingListView(ListView):
    model = LogsOfMailing


def create_mailing(request):
    if request.method == 'POST':
        form = MailingCreateForm(request.POST)
        if form.is_valid():
            mailing = form.save()


            if mailing.frequency.select_frequency == 'один раз в день':
                next_send_date = mailing.date
            elif mailing.frequency.select_frequency == 'один раз в неделю':
                next_send_date = mailing.date + timedelta(weeks=1)
            elif mailing.frequency.select_frequency == 'один раз в месяц':
                next_send_date = mailing.date + timedelta(days=30)
            mailing.next_send_date = next_send_date
            mailing.save()

            scheduler.add_job(send_mailing, 'date', run_date=mailing.next_send_date, args=[mailing.id])

            return redirect('main:home')
    else:
        form = MailingCreateForm()
    return render(request, 'main/mailing_form.html', {'form': form})
