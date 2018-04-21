from django.urls import reverse
from world_cup.models import DatePermissions
from clients.models import Profile
import datetime
from django.utils import timezone
from django.db.models import Q

def date_now(request):
    admin_date = DatePermissions.objects.all().first()
    now = timezone.now()
    ok = False
    if admin_date.start_date == None or admin_date.end_date == None:
        ok = False
    elif admin_date.start_date < now and now < admin_date.end_date:
        ok = True
    else:
        ok = False
    return {'permiso': ok, 'start_date': admin_date.start_date, 'end_date': admin_date.end_date}
