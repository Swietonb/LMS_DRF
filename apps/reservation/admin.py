from django.contrib import admin

# Register your models here.
from apps.reservation.models import Reservation


admin.site.register(Reservation)
