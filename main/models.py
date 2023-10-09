from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from users.models import User


class SelectFrequency(models.Model):
    select_frequency = models.CharField(max_length=50, verbose_name='переодичность')

    def __str__(self):
        return self.select_frequency

    class Meta:
        verbose_name = 'переодичность'
        verbose_name_plural = 'переодичности'


class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='email')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    second_name = models.CharField(max_length=150, verbose_name='фамилия')
    comment = models.CharField(max_length=200, verbose_name='комментарий')
    owner_clients = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='владелец клиента рассылки', null=True,
                              blank=True)

    def __str__(self):
        return f'{self.first_name} {self.second_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name='дата и время рассылки')
    frequency = models.ForeignKey('SelectFrequency', on_delete=models.PROTECT, verbose_name='переодичность рассылки')
    status = models.CharField(default='создана', max_length=50, verbose_name='статус рассылки')
    client = models.ManyToManyField('Client', verbose_name='клиент для рассылки')
    message = models.ForeignKey('Message', on_delete=models.PROTECT, verbose_name='сообщение для рассылки', null=True,
                                blank=True)
    next_send_date = models.DateTimeField(null=True, blank=True, verbose_name='дата следующей рассылки')
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='владелец рассылки', null=True, blank=True)

    def __str__(self):
        return f'{self.date},{self.time}, {self.frequency}, {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Message(models.Model):
    subject_of_letter = models.CharField(max_length=200, verbose_name='тема письма')
    body_of_letter = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.subject_of_letter}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class LogsOfMailing(models.Model):
    date = models.DateTimeField(verbose_name='дата и время логов рассылки')
    status = models.BooleanField(default=False, verbose_name='статус рассылки')
    answer_from_service = models.CharField(max_length=100, verbose_name='ответ от почтового сервера')
    message = models.ForeignKey('Message', on_delete=models.PROTECT, verbose_name='ссылка на сообщение', null=True,
                                blank=True)

    def __str__(self):
        return f'{self.date}, {self.time}, {self.status}, {self.answer_from_service}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'


class CustomPermissions(models.Model):
    class Meta:
        permissions = [("can_disable_mailing", "Can disable mailing")]
