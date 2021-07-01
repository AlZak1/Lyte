from django.conf.urls import url
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TierView, TicketView, ReservationView, TicketRequestView, TicketRequestAPI, TicketPerformanceAPI, RequestTimeView

router = DefaultRouter()

router.register('tiers', TierView)
router.register('tickets', TicketView)
router.register('reservations', ReservationView)
router.register('ticket-requests', TicketRequestView)
router.register('processing-time', RequestTimeView)

urlpatterns = [
    url('api/v1/ticket-requests', TicketRequestAPI.as_view()),
    url('api/v1/performance', TicketPerformanceAPI.as_view())
] + router.urls