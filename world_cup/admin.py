from django.contrib import admin
from .models import Team, RealMatch, UserMatch, UserTeam

# Register your models here.
def set_team_points(team):
    print(team)
    return

def give_real_points(modeladmin, request, queryset):
    for match in queryset:
        if match.played == True and match.phase == 'Groups':
            set_team_points(match.winner)
        else:
            print("No se calcula puntajes")
give_real_points.short_description = 'show match'

class RealMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'penals_team_one',
                    'penals_team_two','played']
    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two',
                        'winner', 'loser')
    actions = [give_real_points]

# Register your models here.
admin.site.register(Team)
admin.site.register(UserMatch)
admin.site.register(UserTeam)
admin.site.register(RealMatch, RealMatchAdmin)
