from django import forms

from main.models import Mailing, Client, Message


class MailingCreateForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Mailing
        fields = ('date', 'frequency', 'message', 'clients')

    def save(self, commit=True):
        mailing = super().save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        mailing.client.set(self.cleaned_data['clients'])
        return mailing


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'first_name', 'second_name', 'comment',)


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
