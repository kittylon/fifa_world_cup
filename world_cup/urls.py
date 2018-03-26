from django.contrib import  admin
from django.urls import path
from django.views.generic import TemplateView
from world_cup.views import (
GroupsView, SummaryGroupsView, EightsView, SummaryEightsView
# , GroupDetailView
)

urlpatterns = [
    path('fase_grupos/', GroupsView.as_view(), name='groups_phase'),
    path('resumen_grupos/', SummaryGroupsView.as_view(), name='groups_summary'),
    path('fase_octavos/', EightsView.as_view(), name='eights_phase'),
    path('resumen_octavos/', SummaryEightsView.as_view(), name='eights_summary'),
    # path('grupos/<str:query>/', GroupDetailView.as_view(), name="group_detail"),
]
