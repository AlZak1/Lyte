from django.db import models


class Tier(models.Model):
    name = models.CharField('Name', max_length=256, blank=True, null=True)
    price = models.DecimalField('Price', max_digits=5, decimal_places=2, blank=True, null=True)
    transfer_fee_percent = models.DecimalField('Fee', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Tier'
        verbose_name_plural = 'Tiers'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    FREE, SOLD = range(2)

    STATUS_CHOICES = (
        (FREE, 'Free'),
        (SOLD, 'Sold')
    )

    tier_id = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True)
    status = models.PositiveSmallIntegerField('Status', choices=STATUS_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Reservation(models.Model):
    email = models.EmailField('Email', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return self.email


class TicketRequest(models.Model):
    tier_id = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Ticket Request'
        verbose_name_plural = 'Ticket Requests'


class RequestTime(models.Model):
    processing_time = models.DecimalField('Time', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Time'
        verbose_name_plural = 'Times'

    def __str__(self):
        return str(self.processing_time)
