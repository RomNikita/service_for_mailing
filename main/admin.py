from django.contrib import admin

from main.models import SelectFrequency, Message, Client


@admin.register(SelectFrequency)
class SelectFrequencyAdmin(admin.ModelAdmin):
    list_display = ('select_frequency',)

@admin.register(Message)
class MessageFrequencyAdmin(admin.ModelAdmin):
    list_display = ('subject_of_letter', 'body_of_letter', 'mailing',)


@admin.register(Client)
class ClientFrequencyAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'second_name', 'comment',)