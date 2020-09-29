from django.urls import path

from . import views
from .views import line_chart, line_chart_json, avg_pot_line_chart, line_chart_avg_pot_json, pct_flop_line_chart, line_chart_pct_flop_json, line_chart_num_plrs_pred_json
from .views import line_chart_num_plrs_pred_cvx_json
from .views import get_name
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='index'),
    path('chart', line_chart, name='line_chart'),
    path('avg_pot', avg_pot_line_chart, name='line_chart_avg_pot'),
    path('pct_flop', pct_flop_line_chart, name='line_chart_avg_pot'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('avg_potJSON', line_chart_avg_pot_json, name='line_chart_avg_pot_json'),
    path('pct_flopJSON', line_chart_pct_flop_json, name='line_chart_pct_flop_json'),
    path('num_plrs_predJSON', line_chart_num_plrs_pred_json, name='line_chart_num_plrs_pred_json'),
    path('num_plrs_pred_cvxJSON', line_chart_num_plrs_pred_cvx_json, name='line_chart_num_plrs_pred_cvx_json'),
    path('your_name', get_name, name='your_name'),
    # path('poker_data_grabber', TemplateView.as_view(template_name = 'blog.html'), name='poker_data_grabber'),    
    path('blog', views.PostList.as_view(), name='home'),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('poker_data/', TemplateView.as_view(template_name = 'poker_data_grabber.html'), name='poker_data_grabber'),
    path('poker_data/', TemplateView.as_view(template_name = 'poker_data_grabber.html'), name='poker_data_grabber'),
]
