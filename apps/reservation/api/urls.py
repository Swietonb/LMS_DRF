from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reservation.api.views import ReservationViewSet

router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservation')


urlpatterns = [
    path('', include(router.urls))
]
