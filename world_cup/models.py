from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    emoji = models.CharField(max_length=255, default=' ')

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
    emoji = models.CharField(max_length=255, default=' ')

    def __str__(self):
        return self.country

class RealMatch(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Fourths','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))
    label = models.CharField(max_length=50, null=False, blank= True, editable=True)
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
    penals_team_one = models.PositiveIntegerField(default=0, blank=True, null=True)
    penals_team_two = models.PositiveIntegerField(default=0,  blank=True, null=True)
    played = models.BooleanField(default=False)
    winner = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                related_name='real_winner')
    loser = models.ForeignKey(
                'world_cup.Team',
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                related_name='real_loser')

    def __str__(self):
        return self.label + '_' + str(self.team_one) + '_vs._' + str(self.team_two)

    class Meta:
        verbose_name = 'RealMatch'
        verbose_name_plural = 'RealMatches'

    @staticmethod
    def update_team(team, points, goals_favor, goals_against):
        team.points += int(points)
        team.goals_favor += int(goals_favor)
        team.goals_against += int(goals_against)
        team.save()
        return

    @staticmethod
    def define_points(real_match):
        points_one = 0
        points_two = 0
        winner = ''
        loser = ''
        if int(real_match.team_one_score) + int(real_match.penals_team_one) == int(real_match.team_two_score) + int(real_match.penals_team_two):
            points_one = 1
            points_two = 1
            if "Groups" not in realmatch.label:
                realmatch.gambled = False
        elif int(real_match.team_one_score) + int(real_match.penals_team_one) > int(real_match.team_two_score) + int(real_match.penals_team_two):
            points_one = 3
            points_two = 0
            real_match.winner = real_match.team_one
            real_match.loser = realmatch.team_two
        else:
            points_one = 0
            points_two = 3
            real_match.winner = real_match.team_two
            real_match.loser = realmatch.team_one

        if "Groups" in label:
            RealMatch.update_team(real_match.team_one, points_one, real_match.team_one_score, real_match.team_two_score)
            RealMatch.update_team(real_match.team_two, points_two, real_match.team_two_score, real_match.team_one_score)
        return

    def save(self, *args, **kwargs):
        if self.played == True:
            RealMatch.define_points(self)
        super(RealMatch, self).save(*args, **kwargs)

class UserMatch(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Fourths','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))

    label = models.CharField(max_length=50, null=False, blank= True, editable=False)
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
    penals_team_one = models.PositiveIntegerField(default=0, blank=True, null=True)
    penals_team_two = models.PositiveIntegerField(default=0,  blank=True, null=True)
    gambled = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)
    winner = models.ForeignKey(
                'world_cup.UserTeam',
                on_delete=models.SET_NULL,
                null=True,
                related_name='user_winner')
    loser = models.ForeignKey(
                'world_cup.UserTeam',
                on_delete=models.SET_NULL,
                null=True,
                related_name='user_loser')

    def __str__(self):
        return self.label + "_" + str(self.user)

    class Meta:
        verbose_name = 'UserMatch'
        verbose_name_plural = 'UserMatches'
