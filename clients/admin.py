from django.contrib import admin
from .models import Client, Profile, TermsConditions

class ClientAdmin(admin.ModelAdmin):
    list_display = ['nit', 'name', 'prof']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'document_type', 'document_number', 'city',
                    'phone', 'mobile', 'address', 'sex', 'company', 'job_title', 'active',
                    'groups_points', 'eights_points', 'fourths_points', 'semi_points',
                    'trd_fth_points', 'final_points', 'total_points', 'groups_filled',
                    'eights_filled', 'fourths_filled', 'semi_filled', 'trd_fth_filled',
                    'final_filled']

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TermsConditions)
