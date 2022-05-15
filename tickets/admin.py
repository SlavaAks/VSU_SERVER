from django.contrib import admin

from tickets.models import *


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['topic', 'description', 'status', 'created']
