from django.db import models

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

    match = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, null=False)
    team_one = models.CharField(max_length=255)
    team_two = models.CharField(max_length=255)
    goals_one = models.PositiveIntegerField()
    goals_two = models.PositiveIntegerField()
