from .models import Ticket, Tier, Reservation, TicketRequest, RequestTime
from rest_framework import serializers


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class TicketRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRequest
        fields = '__all__'


class TicketReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    ticket_requests = TicketRequestSerializer(many=True)

    class Meta:
        fields = '__all__'


class RequestTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestTime
        fields = '__all__'
