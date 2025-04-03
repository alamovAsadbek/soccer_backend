from rest_framework import serializers
from .models import Championship, Match, Team
from fields.serializers import FieldSerializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'description']


class MatchSerializer(serializers.ModelSerializer):
    team1_name = serializers.CharField(source='team1.name', read_only=True)
    team2_name = serializers.CharField(source='team2.name', read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'team1', 'team2', 'team1_name', 'team2_name',
                  'date_time', 'score1', 'score2', 'status']


class ChampionshipSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = Championship
        fields = ['id', 'name', 'description', 'start_date', 'end_date',
                  'field', 'field_name', 'teams', 'matches', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
