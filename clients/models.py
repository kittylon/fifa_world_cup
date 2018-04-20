from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from world_cup.models import Team, RealMatch, UserMatch, UserTeam

# Create your models here.
class TermsConditions(models.Model):
    text = models.TextField()

class Client(models.Model):
    PROFILE_CHOICES = (('10','A'), ('5','B'), ('3','C'))

    nit = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True, default='')
    legal = models.CharField(max_length=255, null=True, blank=True, default='')
    city = models.CharField(max_length=255, null=True, blank=True, default='')
    address = models.CharField(max_length=255, null=True, blank=True, default='')
    phone = models.CharField(max_length=255)
    prof = models.CharField(max_length=50, choices=PROFILE_CHOICES, null=False)

    def __str__(self):
        return (self.name + ' - ' + self.legal)

class Profile(models.Model):
    ID_CHOICES = (('CC','Cédula'), ('PA','Pasaporte'), ('CE','Cédula de extranjería'))
    SEX_CHOICES = (('M','Masculino'), ('F','Femenino'))

    email = models.EmailField(max_length=254, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    document_type = models.CharField(max_length=50, choices=ID_CHOICES, null=False, default='CC')
    document_number = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=50, blank=True, default='')
    phone = models.IntegerField(null=True)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=100, blank=True, default='')
    sex = models.CharField(max_length=100, choices=SEX_CHOICES, null=False, default='M')
    company = models.ForeignKey(
        'clients.Client',
        on_delete=models.SET_NULL,
        null=True,
        related_name = 'users'
    )
    job_title = models.CharField(max_length=200, blank=True, default='')
    active = models.BooleanField(default=True, null=False)
    groups_points = models.PositiveIntegerField(blank=True, default=0)
    eights_points = models.PositiveIntegerField(blank=True, default=0)
    fourths_points = models.PositiveIntegerField(blank=True, default=0)
    semi_points = models.PositiveIntegerField(blank=True, default=0)
    trd_fth_points = models.PositiveIntegerField(blank=True, default=0)
    final_points = models.PositiveIntegerField(blank=True, default=0)
    total_points = models.PositiveIntegerField(blank=True, default=0)
    groups_filled = models.BooleanField(default=False, null=False)
    eights_filled = models.BooleanField(default=False, null=False)
    fourths_filled = models.BooleanField(default=False, null=False)
    semi_filled = models.BooleanField(default=False, null=False)
    trd_fth_filled = models.BooleanField(default=False, null=False)
    final_filled = models.BooleanField(default=False, null=False)

    @staticmethod
    def create_basematch(user):
        real_matches = RealMatch.objects.all()
        all_teams = Team.objects.all()
        real = user.is_superuser
        for team in all_teams:
            new_user_team = UserTeam(real=real,
                                    country = team.country,
                                    group = team.group,
                                    user=user,
                                    emoji=team.emoji)
            new_user_team.save()
        user_teams = UserTeam.objects.filter(user=user)
        team_one_user = ''
        team_two_user = ''
        for real_match in real_matches:

                for team in user_teams:
                    if real_match.team_one.country == team.country:
                        team_one_user = team

                    elif real_match.team_two.country == team.country:
                        team_two_user = team

                    if team_one_user != '' and team_two_user != '':
                        new_user_match = UserMatch(real=real,
                                                    label=real_match.label,
                                                    date=real_match.date,
                                                    phase=real_match.phase,
                                                    group=real_match.group,
                                                    team_one=team_one_user,
                                                    team_two=team_two_user,
                                                    user=user)
                        new_user_match.save()
                        team_one_user = ''
                        team_two_user = ''
        return
#Para la extensión de los usuarios, esto se debe tener antes de la creación del super usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Profile.create_basematch(instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
