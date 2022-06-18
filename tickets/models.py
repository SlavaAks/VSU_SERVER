from django.db import models

from users.models import User
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):

    class StatusChoises(models.TextChoices):
        STATUS_SOLVED = 'solved', _('Тикет решен')
        STATUS_UNSOLVED = 'unsolved',_('Тикет не решен')
        STATUS_FROZEN = 'frozen',_('Тикет заморожен')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус тикета', choices=StatusChoises.choices,
                           default=StatusChoises.STATUS_UNSOLVED)


    class Meta:
        ordering = ('created',)
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    def __str__(self):
        return self.topic


class TicketResponse(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        ordering = ('data',)
        verbose_name = 'response'
        verbose_name_plural = 'responses'
