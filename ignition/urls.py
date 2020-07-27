from django.urls import path

from . import views
from .views import line_chart, line_chart_json, avg_pot_line_chart, line_chart_avg_pot_json, pct_flop_line_chart, line_chart_pct_flop_json

urlpatterns = [
    path('', views.index, name='index'),
    path('chart', line_chart, name='line_chart'),
    path('avg_pot', avg_pot_line_chart, name='line_chart_avg_pot'),
    path('pct_flop', pct_flop_line_chart, name='line_chart_avg_pot'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('avg_potJSON', line_chart_avg_pot_json, name='line_chart_avg_pot_json'),
    path('pct_flopJSON', line_chart_pct_flop_json, name='line_chart_pct_flop_json'),
]