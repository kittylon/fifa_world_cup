from django.contrib import admin
from .models import Team, RealMatch, UserMatch, UserTeam, DatePermissions
from clients.models import Profile

# def check_groups(modeladmin, request, queryset):
#         matches = RealMatch.objects.filter(played=True, phase='Groups').count()
#         all = RealMatch.objects.filter(phase='Groups').count()
#         profile = Profile.objects.get(pk=1)
#         print(profile.user)
#         if matches == all:
#             if user.profile.groups_filled == True:
#                 print('Fase terminada')
#         else:
#             # if user.profile.groups_filled == True:
#             print('Fase no terminada')
# check_groups.short_description = 'check groups'

class RealMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'penals_team_one',
                    'penals_team_two','played']
    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two',
                        'winner', 'loser')
    # actions = [check_groups]

class UserTeamAdmin(admin.ModelAdmin):
    list_display = ['country', 'user']
    readonly_fields = ('country', 'user')


# Register your models here.
admin.site.register(Team)
admin.site.register(UserMatch)
admin.site.register(DatePermissions)
admin.site.register(UserTeam, UserTeamAdmin)
admin.site.register(RealMatch, RealMatchAdmin)
