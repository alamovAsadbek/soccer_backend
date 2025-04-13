import json

from rest_framework import serializers

from fields.models import TimeSlot, Field, Booking, FieldImages


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'field', 'date', 'start', 'user_full_name', 'user_phone', 'end', 'price', 'is_booked']


class FieldImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldImages
        fields = ['id', 'image']


from rest_framework import serializers


class FieldSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Field
        fields = [
            'id', 'name', 'description', 'address', 'contact',
            'surface', 'size', 'owner_name', 'working_days',
            'images', 'uploaded_images',
            'time_slots', 'created_at', 'price_per_hour'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(img.image.url) for img in obj.images.all()]

    def to_internal_value(self, data):
        data = data.copy()

        working_days = data.get('working_days')

        if isinstance(working_days, list) and len(working_days) == 1 and isinstance(working_days[0], dict):
            working_days = working_days[0]

        elif isinstance(working_days, str):
            try:
                working_days = json.loads(working_days)
            except json.JSONDecodeError:
                raise serializers.ValidationError({'working_days': 'Invalid JSON format.'})

        if isinstance(working_days, list):
            all_days = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
            data['working_days'] = {day: (day in working_days) for day in all_days}
            print(data)
        elif isinstance(working_days, dict):
            data['working_days'] = working_days

        else:
            raise serializers.ValidationError({'working_days': 'Invalid format. Must be list or dict.'})

        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        wd = rep.get('working_days', {})
        if isinstance(wd, dict):
            rep['working_days'] = [day for day, value in wd.items() if value]
        return rep

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        field = Field.objects.create(**validated_data)
        for image in uploaded_images:
            FieldImages.objects.create(field=field, image=image)
        return field

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if uploaded_images:
            instance.images.all().delete()
            for image in uploaded_images:
                FieldImages.objects.create(field=instance, image=image)

        return instance


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'time_slot', 'user', 'status', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
