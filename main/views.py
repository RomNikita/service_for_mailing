from datetime import timedelta
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from blog.models import Blog
from main.forms import MailingCreateForm, ClientCreateForm, MessageCreateForm
from main.models import Mailing, Client, Message, LogsOfMailing
from main.runapscheduler import scheduler, send_mailing, schedule_mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mail_list')
    template_name = 'main/mailing_confirm_delete.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientCreateForm
    success_url = reverse_lazy('main:client_list')

    def form_valid(self, form):
        form.instance.owner_clients = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')

    def get_queryset(self):
        return Client.objects.filter(owner_clients=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/client_list.html'

    def get_queryset(self):
        return Client.objects.filter(owner_clients=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageCreateForm
    success_url = reverse_lazy('main:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class LogsOfMailingListView(LoginRequiredMixin, ListView):
    model = LogsOfMailing


@login_required
def create_mailing(request):
    if request.method == 'POST':
        form = MailingCreateForm(request.POST, request=request)
        if form.is_valid():
            mailing = form.save(commit=False)

            if mailing.frequency.select_frequency == 'один раз в день':
                next_send_date = mailing.date + timedelta(days=1)
            elif mailing.frequency.select_frequency == 'один раз в неделю':
                next_send_date = mailing.date + timedelta(weeks=1)
            elif mailing.frequency.select_frequency == 'один раз в месяц':
                next_send_date = mailing.date + timedelta(days=30)

            mailing.next_send_date = next_send_date
            mailing.save()

            recipients = form.cleaned_data['clients'].values_list('email', flat=True)

            schedule_mailing(mailing.id, mailing.next_send_date, mailing.frequency.select_frequency, recipients)

            send_mailing(mailing.id, recipients)

            return redirect('main:mail_list')
    else:
        clients = Client.objects.all()
        form = MailingCreateForm(initial={'clients': clients}, request=request)
    return render(request, 'main/mailing_form.html', {'form': form})



def home(request):
    total_mailings = Mailing.objects.count()

    active_mailings = Mailing.objects.filter(status='активна').count()

    unique_clients = Client.objects.filter(mailing__isnull=False).distinct().count()

    blog =Blog.objects.all()
    random_blog = random.sample(list(blog), min(len(blog), 3))

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_blog': random_blog,
    }

    return render(request, 'main/home.html', context)

