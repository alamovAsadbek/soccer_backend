from django.contrib import admin
from .models import Field, TimeSlot, Booking

admin.site.site_header = 'Football Field Admin Panel'
admin.site.site_title = 'Football Field Admin'

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'size', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'contact', 'size',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'Field Models'
        verbose_name = 'Field Model'

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('field', 'price', 'date', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('field', 'price', 'date',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'TimeSlot Models'
        verbose_name = 'TimeSlot Model'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('time_slot', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('time_slot', 'user', 'status',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'Booking Models'
        verbose_name = 'Booking Model'
