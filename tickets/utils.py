from rest_framework import serializers

from EducationApp.settings import status_ticket
from tickets.models import Ticket, TicketResponse


class JeneralMixin:
    def change_status(request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if 'status' in request.data.keys():

                if request.data['status'] in status_ticket:
                    ticket.status = request.data['status']
                    ticket.save()
                    return ticket
                else:
                    raise serializers.ValidationError("THIS STATUS IS NOT VALUABLE")
            else:
                raise serializers.ValidationError("Must include fields 'status' ")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("ticket is not exists")

    def obtain_response(ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            try:
                resp = TicketResponse.objects.get(ticket=ticket)
                return resp
            except TicketResponse.DoesNotExist:
                raise serializers.ValidationError("this in ticket have not a response")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("ticket is not exists")
