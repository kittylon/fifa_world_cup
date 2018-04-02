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
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Cuartos','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))
    label = models.CharField(max_length=50, null=False, blank= True, editable=False)
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

    def __str__(self):
        return self.label + '_' + str(self.team_one) + '_vs._' + str(self.team_two)

    class Meta:
        verbose_name = 'RealMatch'
        verbose_name_plural = 'RealMatches'

    @staticmethod
    def score_groups(user):
        eights_score = 0
        played_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Groups')
        for match in played_matches:
            eights_score += match.points

        user.profile.eights_points = eights_score
        user.save()
        print(str(user.first_name) + " " + str(user.profile.eights_points))
        return

    @staticmethod
    def points_user_match(label, team_one_score, team_two_score):
        gambled_matches = UserMatch.objects.filter(label=label, gambled=True)
        for match in gambled_matches:
            if match.team_one_score == team_one_score \
            and match.team_two_score == team_two_score:
                match.points = 3
            elif (match.team_one_score > match.team_two_score and team_one_score > team_two_score) \
            or (match.team_one_score < match.team_two_score and team_one_score < team_two_score):
                match.points = 1
            else:
                match.points = 0

            match.save()
            RealMatch.score_groups(match.user)

        return

    @staticmethod
    def save_groups():
        played_groups = RealMatch.objects.filter(phase='Groups', played=True).count()
        groups_matches = RealMatch.objects.filter(phase='Groups').count()

        if groups_matches == played_groups:
            print("create groups")
        else:
            print("Not allowed to create groups yet")
        return


    def save(self, *args, **kwargs):
        winner = None
        if self.played == True:
            RealMatch.points_user_match(self.label, self.team_one_score, self.team_two_score)
            if self.phase == 'Groups':
                RealMatch.save_groups()


        super(RealMatch, self).save(*args, **kwargs)

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
    penals_team_one = models.PositiveIntegerField(default=0, blank=True, null=True)
    penals_team_two = models.PositiveIntegerField(default=0,  blank=True, null=True)
    gambled = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.label + "_" + str(self.user)

    class Meta:
        verbose_name = 'UserMatch'
        verbose_name_plural = 'UserMatches'
