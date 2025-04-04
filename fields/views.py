from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Field, TimeSlot, Booking
from .serializers import FieldSerializer, TimeSlotSerializer, BookingSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("User not authenticated")

        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user(self, request):
        fields = Field.get_user_fields(request.user.id)
        serializer = self.get_serializer(fields, many=True)
        return Response(serializer.data)


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        field_id = self.request.query_params.get('field_id')
        date = self.request.query_params.get('date')

        queryset = TimeSlot.objects.all()

        if field_id:
            queryset = queryset.filter(field_id=field_id)

        if date:
            queryset = queryset.filter(date=date)

        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.isAdmin:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        time_slot = serializer.validated_data['time_slot']
        time_slot.is_booked = True
        time_slot.booked_by = self.request.user
        time_slot.save()
        serializer.save(user=self.request.user)
