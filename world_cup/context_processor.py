from django.urls import reverse
from world_cup.models import RealMatch, UserMatch, Team

def Teams_data(request):
    teams = Team.objects.all()
    return {'teams': teams}

# def UserMatch_data(request):
#     user_matches = UserMatch.objects.filter(user=request.user)
#     return {'user_matches': user_matches}
