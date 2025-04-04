from rest_framework import serializers

from fields.models import TimeSlot, Field, Booking


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'field', 'date', 'start', 'end', 'price', 'is_booked']


class FieldSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Field
        fields = ['id', 'name', 'description', 'address', 'contact',
                  'surface', 'size', 'amenities', 'working_days', 'images',
                  'lat', 'lng', 'time_slots', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'time_slot', 'user', 'status', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
