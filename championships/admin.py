from django.contrib import admin
from .models import Team, Championship, Match

admin.site.site_header = 'Football Field Admin Panel'
admin.site.site_title = 'Football Field Admin'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'captain', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'captain',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'Team Models'
        verbose_name = 'Team Model'

@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'field', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'field',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'Championship Models'
        verbose_name = 'Championship Model'

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('championship', 'team1', 'team2', 'date_time', 'status', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('championship', 'team1', 'team2', 'date_time', 'status',)
    ordering = ('-created_at', '-updated_at')
    readonly_fields = ('created_at', 'updated_at')

    class Meta:
        verbose_name_plural = 'Match Models'
        verbose_name = 'Match Model'