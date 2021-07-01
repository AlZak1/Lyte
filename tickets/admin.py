from django.contrib import admin
from .models import Ticket, Tier, Reservation, TicketRequest, RequestTime

admin.site.register(Tier)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(TicketRequest)
admin.site.register(RequestTime)
