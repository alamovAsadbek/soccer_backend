from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, TimeSlotViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'fields', FieldViewSet)
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]