from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Client(models.Model):
    PROFILE_CHOICES = (('5_Participantes','A'), ('2_Participantes','B'), ('1_Participante','C'))

    nit = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile = models.CharField(max_length=50, choices=PROFILE_CHOICES, null=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    ID_CHOICES = (('CC','Cédula'), ('PA','Pasaporte'), ('CE','Cédula de extranjería'))

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
    total_points = models.PositiveIntegerField(blank=True, default=0)
    fill_groups = models.BooleanField(default=False, null=False)


#Para la extensión de los usuarios, esto se debe tener antes de la creación del super usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
