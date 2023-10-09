from django.urls import path
from django.views.decorators.cache import cache_page

from main.views import MailingDeleteView, MailingListView, ClientCreateView, MessageCreateView, \
    ClientDeleteView, ClientListView, MessageListView, MessageDeleteView, create_mailing, LogsOfMailingListView, home

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('mail/', MailingListView.as_view(), name='mail_list'),
    path('mail/create', cache_page(60)(create_mailing), name='mail_create'),
    path('mail/delete/<int:pk>/', MailingDeleteView.as_view(), name='mail_delete'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('logs/', LogsOfMailingListView.as_view(), name='logs_list')
]