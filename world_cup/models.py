from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from django.db.models import Q

# Create your models here.
class DatePermissions(models.Model):
    start_date =  models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)

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
    real = models.BooleanField(default=False, null=False)
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

class UserMatch(models.Model):
    PHASE_CHOICES = (('Groups','Grupos'), ('Eights','Octavos'), ('Fourths','Cuartos'),
                    ('Semi','Semifinal'),('3y4','Puesto 3 y 4'), ('Finals','Final'))

    GROUP_CHOICES = (('A','Grupo A'), ('B','Grupo B'), ('C','Grupo C'),
                    ('D','Grupo D'), ('E','Grupo E'), ('F','Grupo F'),
                    ('G','Grupo G'), ('H','Grupo H'))
    real = models.BooleanField(default=False, null=False)
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

    @staticmethod
    def cal_groups(phase, user):
        groups_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            groups_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                groups_points += match.points
            u.profile.groups_points = groups_points
            u.profile.total_points = u.profile.groups_points + u.profile.eights_points + u.profile.fourths_points + u.profile.semi_points + u.profile.trd_fth_points + u.profile.final_points
            u.save()

    @staticmethod
    def cal_eights(phase, user):
        eights_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            eights_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                eights_points += match.points
            u.profile.eights_points = eights_points
            u.profile.total_points = u.profile.groups_points + u.profile.eights_points + u.profile.fourths_points + u.profile.semi_points + u.profile.trd_fth_points + u.profile.final_points
            u.save()

    @staticmethod
    def cal_fourhts(phase, user):
        fourths_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            fourths_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                fourths_points += match.points
            u.profile.fourths_points = fourths_points
            u.profile.total_points = u.profile.groups_points + u.profile.eights_points + u.profile.fourths_points + u.profile.semi_points + u.profile.trd_fth_points + u.profile.final_points
            u.save()

    @staticmethod
    def cal_semi(phase, user):
        semi_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            semi_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                semi_points += match.points
            u.profile.semi_points = semi_points
            u.profile.total_points = u.profile.groups_points + u.profile.eights_points + u.profile.fourths_points + u.profile.semi_points + u.profile.trd_fth_points + u.profile.final_points
            u.save()

    @staticmethod
    def cal_thrd_fourth(phase, user):
        trd_fth_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            trd_fth_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                trd_fth_points += match.points
            u.profile.trd_fth_points = trd_fth_points
            u.profile.total_points = u.profile.groups_points + u.profile.eights_points + u.profile.fourths_points + u.profile.semi_points + u.profile.trd_fth_points + u.profile.final_points
            u.save()

    @staticmethod
    def cal_final(phase, user):
        final_points = 0
        users = User.objects.filter(~Q(username=user))
        for u in users:
            final_points = 0
            user_matches = UserMatch.objects.filter(phase=phase, user=u)
            for match in user_matches:
                final_points += match.points
            u.profile.final_points = final_points
            u.save()

    @staticmethod
    def check_phase(phase, user):
        print(phase)
        if "Groups" in phase:
            UserMatch.cal_groups(phase, user)
        if "Eights" in phase:
            UserMatch.cal_eights(phase, user)
        elif "Fourths" in phase:
            UserMatch.cal_fourhts(phase, user)
        elif "Semi" in phase:
            UserMatch.cal_semi(phase, user)
        elif "3y4" in phase:
            UserMatch.cal_thrd_fourth(phase, user)
        elif "Finals" in phase:
            UserMatch.cal_final(phase, user)
        else:
            print("Label no válido" + ' ' + phase)
        return

    @staticmethod
    def cal_points(match):
        user_matches = UserMatch.objects.filter(Q(label=match.label, gambled=True) & ~Q(user=match.user))
        for u_match in user_matches:
            if match.team_one.country == u_match.team_one.country and match.team_two.country == u_match.team_two.country:
                if match.phase == 'Groups':
                    print('Fucked')
                    if match.team_one_score == u_match.team_one_score and match.team_two_score == u_match.team_two_score:
                        print('Jodida A')
                        u_match.points = 3
                        u_match.save()
                    elif str(match.winner) == str(u_match.winner) and str(match.loser) == str(u_match.loser):
                        print('Jodida B')
                        print(match.team_one_score)
                        print(u_match.team_one_score)
                        print(match.team_two.country)
                        print(u_match.team_two.country)
                        u_match.points = 1
                        u_match.save()
                        print('Obtienes un punto')
                    else:
                        print('Jodida C')
                        u_match.points = 0
                        u_match.save()
                else:
                    print('OVER')
                    if match.team_one_score == u_match.team_one_score and match.team_two_score == u_match.team_two_score:
                        if (match.penals_team_one > 0  or match.penals_team_two > 0) and (str(match.winner) == str(u_match.winner) and str(match.loser) == str(u_match.loser)):
                            u_match.points = 4
                            u_match.save()
                        else:
                            u_match.points = 3
                            u_match.save()
                    elif str(match.winner) == str(u_match.winner) and str(match.loser) == str(u_match.loser):
                        u_match.points = 1
                        u_match.save()
                        print('Obtienes un punto')
                    else:
                        u_match.points = 0
                        u_match.save()
            else:
                print('No le atinaste al pronóstico de los jugadores')
        UserMatch.check_phase(match.phase, match.user)


@receiver(post_save, sender=UserMatch)
def create_user_profile(sender, instance, created, **kwargs):
    if str(instance.user.username) == 'polla_admin':
        print('Calcular puntos de todo el mundo')
        UserMatch.cal_points(instance)
