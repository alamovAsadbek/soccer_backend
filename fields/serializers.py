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
            'lat', 'lng', 'time_slots', 'created_at', 'price_per_hour'
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(img.image.url) for img in obj.images.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # faqat true bo'lgan kunlarni yuborish
        working_days_dict = instance.working_days or {}
        # JSON fieldni listdan dictga o'zgartirish
        data['working_days'] = [day for day, val in working_days_dict.items() if val]
        return data

    def to_internal_value(self, data):
        data = data.copy()
        working_days_list = data.get('working_days', [])
        # faqat tanlangan kunlarni true qilib saqlaymiz
        if isinstance(working_days_list, list):
            all_days = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
            data['working_days'] = {day: (day in working_days_list) for day in all_days}
        return super().to_internal_value(data)

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
