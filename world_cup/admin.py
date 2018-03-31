from django.contrib import admin
from .models import Team, RealMatch, UserMatch, UserTeam

# Register your models here.
def give_real_points(modeladmin, request, queryset):
    for match in queryset:
        if match.played == True:
            print(match.label)
        else:
            print("No se ha jugado ese partido")
give_real_points.short_description = 'show match'

class RealMatchAdmin(admin.ModelAdmin):
    list_display = ['label', 'date', 'phase', 'group', 'team_one', 'team_two',
                    'team_one_score', 'team_two_score', 'played']
    readonly_fields = ('label', 'date', 'phase', 'group', 'team_one', 'team_two')
    actions = [give_real_points]

# Register your models here.
admin.site.register(Team)
admin.site.register(UserMatch)
admin.site.register(UserTeam)
admin.site.register(RealMatch, RealMatchAdmin)
