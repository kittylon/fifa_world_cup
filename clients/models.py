from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Team(models.Model):
    GROUP_CHOICES = (('GROUP_A','A'), ('GROUP_B','B'), ('GROUP_C','C'), ('GROUP_D','D'),
                    ('GROUP_E','E'), ('GROUP_F','F'), ('GROUP_G','G'), ('GROUP_H','H'))

    country = models.CharField(max_length=255)
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, null=False)

    def __str__(self):
        return self.country

class Client(models.Model):
    PROFILE_CHOICES = (('5_Participantes','A'), ('2_Participantes','B'), ('1_Participante','C'))

    nit = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile = models.CharField(max_length=50, choices=PROFILE_CHOICES, null=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    ID_CHOICES = (('Cédula','CC'), ('Pasaporte','PA'), ('Cedula_extranjería','CE'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    document_type = models.CharField(max_length=50, choices=ID_CHOICES, null=False, default='CC')
    document_number = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=50, blank=True, default='')
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=100, blank=True, default='')
    company = models.ForeignKey(
        'clients.Client',
        on_delete=models.SET_NULL,
        null=True,
        related_name = 'users'
    )
    job_title = models.CharField(max_length=200, blank=True, default='')


    def __str__(self):
        return self.user

#Para la extensión de los usuarios, esto se debe tener antes de la creación del super usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
