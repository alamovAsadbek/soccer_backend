from rest_framework import serializers

from fields.models import TimeSlot, Field, Booking, FieldImages


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'field', 'date', 'start', 'end', 'price', 'is_booked']


class FieldSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    class Meta:
        model = Field
        fields = ['id', 'name', 'description', 'address', 'contact',
                  'surface', 'size', 'amenities', 'working_days', 'images',
                  'lat', 'lng', 'time_slots', 'created_at', 'price_per_hour']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        field = Field.objects.create(**validated_data)
        for image in images:
            FieldImages.objects.create(field=field, image=image)
        return field

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'time_slot', 'user', 'status', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
