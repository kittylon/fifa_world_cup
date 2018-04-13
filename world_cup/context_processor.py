from django.urls import reverse
from world_cup.models import DatePermissions
import datetime
from django.utils import timezone


def Date_Permissions_data(request):
    date_permissions = DatePermissions.objects.get(pk=1)
    return {'date_permissions': date_permissions}

def date_now(request):
    date_permissions = DatePermissions.objects.all()
    now = timezone.now()
    ok = False
    for date in date_permissions:
        if now > date.date:
            ok = False
        else:
            ok = True
    return {'permiso': ok}
