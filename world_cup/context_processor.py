from django.urls import reverse
from world_cup.models import Match, Team

def Teams_data(request):
    teams = Team.objects.all()
    return {'teams': teams}

def Matches_data(request):
    matches = Match.objects.all()
    return {'matches': matches}
