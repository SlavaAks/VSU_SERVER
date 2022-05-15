from rest_framework import serializers

from tickets.models import Ticket, TicketResponse


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'topic', 'description', 'status')
        required = ('topic', 'description')

    def validate(self, attrs):
        credentials = {
            'topic': attrs.get('topic'),
            'description': attrs.get('description')
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include fields:(topic and description)"
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        ticket = Ticket(
            user=validated_data.user,
            topic=validated_data.data['topic'],
            description=validated_data.data['description'],
        )
        print(ticket)
        ticket.save()
        return ticket


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = ('response',)

    def validate(self, attrs):
        credentials = {
            'response': attrs.get('response')
        }

        if all(credentials.values()):
            return credentials
        else:
            msg = "Must include field 'response'"
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        resp = TicketResponse(
            response=validated_data['response'],
            ticket=validated_data['ticket'],
        )
        resp.save()
        return resp

    def add_response_to_ticket(self, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            print(ticket.status == Ticket.STATUS_SOLVED)
            if not ticket.status == Ticket.STATUS_SOLVED:
                data = self.data
                ticket.status = Ticket.STATUS_SOLVED
                ticket.save()
                data['ticket'] = ticket
                resp = self.create(data)
                return self
            else:
                raise serializers.ValidationError("this ticket is solved")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("this ticket is not exist")
