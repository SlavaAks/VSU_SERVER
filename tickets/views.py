from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import *
from tickets.permissions import IsAuthor
from tickets.serializers import TicketSerializer, ResponseSerializer
from tickets.task import send_email_task_after_response, send_email_task_befor_response
from tickets.utils import JeneralMixin
import celery

class APIUserTickets(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = TicketSerializer(Ticket.objects.filter(user=request.user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request)
            # send_email_task_befor_response.apply_async(args=[request.user.email])
            send_email_task_befor_response.delay(request.user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewTickets(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISupportTicket(APIView,JeneralMixin):
    permission_classes = (IsAdminUser,)

    def post(self, request, ticket_id):

        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.add_response_to_ticket(ticket_id)
            send_email_task_after_response.delay(request.user.email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, ticket_id):
        ticket = self.change_status(request, ticket_id)
        serializer=TicketSerializer(ticket)
        return Response(serializer.data,status=status.HTTP_200_OK)




class ViewResponse(APIView,JeneralMixin):
    permission_classes = (IsAuthenticated, IsAuthor)

    def get(self, request, ticket_id):
        resp = self.obtain_response(ticket_id)
        try:
            self.check_object_permissions(resp)
            serializer = ResponseSerializer(resp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
