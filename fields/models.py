from django.db import models

from users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Field(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    contact = models.CharField(max_length=50)
    surface = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    amenities = models.CharField(max_length=255)
    working_days = models.JSONField(default=list)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class FieldImages(BaseModel):
    field = models.ForeignKey(Field, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return f"{self.field.name} - {self.image.name}"


class TimeSlot(BaseModel):
    field = models.ForeignKey(Field, related_name='time_slots', on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('field', 'date', 'start', 'end')

    def __str__(self):
        return f"{self.field.name} - {self.date} {self.start}-{self.end}"


class Booking(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
    )

    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.time_slot}"
