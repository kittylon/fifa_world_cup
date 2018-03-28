from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))

    country = models.CharField(max_length=255)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=False)
    points = models.PositiveIntegerField(default=0)
    goals_favor = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.country

class UserTeam(models.Model):
    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))

    country = models.CharField(max_length=255)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=False)
    points = models.PositiveIntegerField(default=0)
    goals_favor = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User_team')

    def __str__(self):
        return self.country

class RealMatch(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Cuartos','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))
    label = models.CharField(max_length=50, null=False, blank= True)
    date = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, null=False)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=True, blank=True)
    team_one = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                related_name='real_team_one')

    team_two = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                related_name='real_team_two')
    team_one_score = models.PositiveIntegerField(default=0)
    team_two_score = models.PositiveIntegerField(default=0)
    played = models.BooleanField(default=False)

    def __str__(self):
        return self.label

class UserMatch(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Cuartos','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))

    label = models.CharField(max_length=50, null=False, blank= True)
    date = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, null=False)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=True, blank=True)
    team_one = models.ForeignKey(
                'world_cup.UserTeam',
                on_delete=models.SET_NULL,
                null=True,
                related_name='user_team_one')

    team_two = models.ForeignKey(
                'world_cup.UserTeam',
                on_delete=models.SET_NULL,
                null=True,
                related_name='user_team_two')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gambler')
    team_one_score = models.PositiveIntegerField(default=0)
    team_two_score = models.PositiveIntegerField(default=0)
    gambled = models.BooleanField(default=False)

    def __str__(self):
        return self.label + "_" + str(self.user)
