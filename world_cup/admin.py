from django.contrib import admin
from .models import Team, RealMatch, UserMatch, UserTeam
from clients.models import Profile

# Register your models here.
def set_team_points(team):
    print(team)
    return

def check_groups(modeladmin, request, queryset):
        matches = RealMatch.objects.filter(played=True, phase='Groups').count()
        all = RealMatch.objects.filter(phase='Groups').count()
        profile = Profile.objects.get(pk=1)
        print(profile.user)
        if matches == all:
            if user.profile.groups_filled == True:
                print('Fase terminada')
        else:
            # if user.profile.groups_filled == True:
            print('Fase no terminada')
check_groups.short_description = 'check groups'
    # for match in queryset:
    #     if match.played == True and match.phase == 'Groups':
    #         set_team_points(match.winner)
    #     else:
    #         print("No se calcula puntajes")


class RealMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'penals_team_one',
                    'penals_team_two','played']
    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two',
                        'winner', 'loser')
    actions = [check_groups]

# Register your models here.
admin.site.register(Team)
admin.site.register(UserMatch)
admin.site.register(UserTeam)
admin.site.register(RealMatch, RealMatchAdmin)
