from django.db import models

from fields.models import Field
from users.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Team(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='captained_teams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')

    def __str__(self):
        return self.name


class Championship(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='championships')
    teams = models.ManyToManyField(Team, related_name='championships')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='championships')

    def __str__(self):
        return self.name

    # Method to get only championships created by the current user
    @classmethod
    def get_user_championships(cls, user_id):
        return cls.objects.filter(created_by_id=user_id)


class Match(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Rejalashtirilgan'),
        ('in_progress', 'O\'yinda'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
    )

    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='matches')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date_time = models.DateTimeField()
    score1 = models.PositiveSmallIntegerField(null=True, blank=True)
    score2 = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"