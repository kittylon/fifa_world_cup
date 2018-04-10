from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import Q

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
    def save_team_stats(team, points, goals_favor, goals_against):
        team.points = points
        team.goals_favor = goals_favor
        team.goals_against = goals_against
        team.save()
        return

    @staticmethod
    def set_team_stats(team):
        points = 0
        goals_favor = 0
        goals_against = 0
        matches = RealMatch.objects.filter(Q(team_one=team) | Q(team_two=team))
        for match in matches:
            if(match.winner == None):
                points += 1
            elif(match.winner == team):
                points += 3
            if (match.team_one == team):
                goals_favor += match.team_one_score
                goals_against += match.team_two_score
            else:
                goals_favor += match.team_two_score
                goals_against += match.team_one_score
        RealMatch.save_team_stats(team, points, goals_favor, goals_against)
        return

@receiver(post_save, sender=RealMatch)
def save_profile(sender, instance, **kwargs):
    RealMatch.set_team_stats(instance.team_one)
    RealMatch.set_team_stats(instance.team_two)
    return

@receiver(pre_save, sender=RealMatch)
def set_winner(sender, instance, **kwargs):
    if int(instance.team_one_score) + int(instance.penals_team_one) == int(instance.team_two_score) + int(instance.penals_team_two):
        instance.winner = None
        instance.loser = None
        if "Groups" not in instance.label:
            instance.played = False
    elif int(instance.team_one_score) + int(instance.penals_team_one) > int(instance.team_two_score) + int(instance.penals_team_two):
        instance.winner = instance.team_one
        instance.loser = instance.team_two
    else:
        instance.winner = instance.team_two
        instance.loser = instance.team_one

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
