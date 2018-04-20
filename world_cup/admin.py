from django.contrib import admin
from .models import Team, RealMatch, UserMatch, UserTeam, DatePermissions
from clients.models import Profile

class RealMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'penals_team_one',
                    'penals_team_two','played']
    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two',
                        'winner', 'loser')
    search_fields = ['label', 'phase']


class UserMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'user', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'penals_team_one',
                    'penals_team_two','gambled']

    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two',
                        'winner', 'loser')
    search_fields = ['user__username']

class DatePermissionsAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']

class UserTeamAdmin(admin.ModelAdmin):
    list_display = ['country', 'user']
    readonly_fields = ('country', 'user')
    search_fields = ['user__username']

# Register your models here.
admin.site.register(Team)
admin.site.register(DatePermissions, DatePermissionsAdmin)
admin.site.register(UserTeam, UserTeamAdmin)
admin.site.register(RealMatch, RealMatchAdmin)
admin.site.register(UserMatch, UserMatchAdmin)
