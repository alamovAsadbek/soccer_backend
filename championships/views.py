from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Championship, Match, Team
from .serializers import ChampionshipSerializer, MatchSerializer, TeamSerializer
from fields.models import Field


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class ChampionshipViewSet(viewsets.ModelViewSet):
    queryset = Championship.objects.all()
    serializer_class = ChampionshipSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]

    def get_queryset(self):
        return Championship.objects.prefetch_related('teams', 'matches')

    def perform_create(self, serializer):
        # Ensure users can only create championships for their own fields
        field_id = serializer.validated_data.get('field').id
        user = self.request.user

        # If not admin, check if the field belongs to the user
        if not user.isAdmin:
            user_fields = Field.get_user_fields(user.id).values_list('id', flat=True)
            if field_id not in user_fields:
                raise PermissionError("Bu maydonni siz boshqarmaysiz")

        serializer.save(created_by=user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user(self, request):
        championships = Championship.get_user_championships(request.user.id)
        serializer = self.get_serializer(championships, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        championship_id = self.request.query_params.get('championship_id')
        date = self.request.query_params.get('date')

        queryset = Match.objects.all()

        if championship_id:
            queryset = queryset.filter(championship_id=championship_id)

        if date:
            queryset = queryset.filter(date_time__date=date)

        return queryset