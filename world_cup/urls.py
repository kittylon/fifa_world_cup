from django.contrib import  admin
from django.urls import path
from django.views.generic import TemplateView
from world_cup.views import (
GroupsView, SummaryGroupsView, EightsView,
SummaryEightsView, FourthsView, SummaryFourthsView,
SemiView, SummarySemiView, TercerCuartoView,
SummaryTercerCuartoView, SummaryFinalsView,
FinalsView, ReyparAdminView
)

urlpatterns = [
    path('fase_grupos/', GroupsView.as_view(), name='groups_phase'),
    path('resumen_grupos/', SummaryGroupsView.as_view(), name='groups_summary'),
    path('fase_octavos/', EightsView.as_view(), name='eights_phase'),
    path('resumen_octavos/', SummaryEightsView.as_view(), name='eights_summary'),
    path('fase_cuartos/', FourthsView.as_view(), name='fourths_phase'),
    path('resumen_cuartos/', SummaryFourthsView.as_view(), name='fourths_summary'),
    path('fase_semifinal/', SemiView.as_view(), name='semi_phase'),
    path('resumen_semifinal/', SummarySemiView.as_view(), name='semi_summary'),
    path('fase_tercer_cuarto/', TercerCuartoView.as_view(), name='third_fourth_phase'),
    path('resumen_tercer_cuarto/', SummaryTercerCuartoView.as_view(), name='third_fourth_summary'),
    path('fase_final/', FinalsView.as_view(), name='finals_phase'),
    path('resumen_final/', SummaryFinalsView.as_view(), name='finals_summary'),
    path('reypar_admin/', ReyparAdminView.as_view(), name='reypar_admin'),
]
