from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', null=True, blank=True)
    count_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_of_publication = models.DateField(default=timezone.now, verbose_name='дата создания', null=True)

    def __str(self):
        return f'{self.title} {self.date_of_publication} ({self.count_of_views} просм.)'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

