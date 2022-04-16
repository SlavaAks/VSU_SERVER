from django.contrib import admin

from users.models import *


@admin.register(User)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','email','is_staff']