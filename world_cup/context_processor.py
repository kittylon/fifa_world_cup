from django.urls import reverse
from world_cup.models import RealMatch, Team

def Teams_data(request):
    teams = Team.objects.all()
    return {'teams': teams}

def UserMatch_data(request):
    matches = UserMatch.objects.filer(request.user)
    return {'user_matches': user_matches}
