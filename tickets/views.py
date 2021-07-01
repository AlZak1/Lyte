from django.db.models import Avg
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tickets.models import Tier, Ticket, Reservation, TicketRequest, RequestTime
from tickets.serializers import TierSerializer, TicketSerializer, ReservationSerializer, TicketRequestSerializer, \
    TicketReservationSerializer, RequestTimeSerializer

from tickets.time_processing import measure_time


class TierView(ModelViewSet):
    queryset = Tier.objects.all()
    serializer_class = TierSerializer


class TicketView(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationView(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TicketRequestView(ModelViewSet):
    queryset = TicketRequest.objects.all()
    serializer_class = TicketRequestSerializer


class RequestTimeView(ModelViewSet):
    queryset = RequestTime.objects.all()
    serializer_class = RequestTimeSerializer


class TicketRequestAPI(APIView):
    parser_classes = (JSONParser,)
    serializer_class = TicketReservationSerializer

    @measure_time
    def post(self, request):
        response = []
        ticket_request_list = []
        reservation_list = []
        for obj in request.data:
            serializer = TicketReservationSerializer(data=obj)
            if serializer.is_valid():
                reservation_cost = 0
                reservation_fee = 0
                ticket_request = obj.get('ticket_requests')
                for ticket in ticket_request:
                    try:
                        ticket['ticket_id'] = Ticket.objects.get(tier_id=ticket.get('tier_id'), status=0).id
                    except Ticket.DoesNotExist:
                        ticket['ticket_id'] = None
                    reservation_cost += Tier._meta.get_field('price').value_from_object(
                        Tier.objects.get(id=ticket['tier_id']))
                    reservation_fee += Tier._meta.get_field('transfer_fee_percent').value_from_object(
                        Tier.objects.get(id=ticket['tier_id']))
                    obj['reservation_cost'] = reservation_cost
                    obj['reservation_fee'] = reservation_fee
                    ticket_request_list.append(ticket)
                    reservation_list.append(obj)
                response.append(obj)
            else:
                return Response(data='Wrong data', status=status.HTTP_400_BAD_REQUEST)
        empty_ticket_id = [x for x in ticket_request_list if x['ticket_id'] is None]
        if empty_ticket_id:
            return Response(data='Not enough tickets', status=status.HTTP_404_NOT_FOUND)
        else:
            for obj in response:
                serializer = TicketReservationSerializer(data=obj)
                if serializer.is_valid():
                    ticket_request = obj.get('ticket_requests')
                    for ticket in ticket_request:
                        Ticket.objects.filter(id=ticket['ticket_id']).update(status=1)

        return Response(response, status=status.HTTP_200_OK)


class TicketPerformanceAPI(APIView):

    def get(self, request):
        performance_dict = {
            'average_process_time': RequestTime.objects.aggregate(Avg('processing_time'))['processing_time__avg'],
            'requests_count': TicketRequest.objects.all().count()
        }

        return Response(performance_dict, status=status.HTTP_200_OK)
