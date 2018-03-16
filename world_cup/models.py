from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    GROUP_CHOICES = (('A','Grupo A'), ('GROUP_B','Grupo B'), ('GROUP_C','Grupo C'),
                    ('GROUP_D','Grupo D'), ('GROUP_E','Grupo E'), ('GROUP_F','Grupo F'),
                    ('GROUP_G','Grupo G'), ('GROUP_H','Grupo H'))

    country = models.CharField(max_length=255)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=False)

    def __str__(self):
        return self.country

class Match(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Cuartos','Cuartos'),
                    ('Semi','Semifinal'),('3_y_4','Puesto 3 y 4'), ('Finals','Final'))

    date = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, null=False)
    team_one = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                related_name='team_one')

    team_two = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                related_name='team_two')

class UserGuess(models.Model):
    match = models.ForeignKey(
                'world_cup.Match',
                on_delete=models.SET_NULL,
                null=True,
                related_name='match')
    team_one_score = models.PositiveIntegerField()
    team_two_score = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gambler')
