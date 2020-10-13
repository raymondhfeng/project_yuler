from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from ignition.models import IgnitionRow,IgnitionRowPredictionOLS,IgnitionRowPredictionCVX

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import time
from datetime import datetime, timedelta
from time import mktime
from statsmodels.regression.linear_model import OLSResults

NUM_TICKS = 60

def index(request):
	return render(request, 'home.html')

class LineChartJSONView(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        two_hours = [str(elem['pub_date'])[10:19] for elem in two_hours]
        return two_hours

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1]
        #two_hours = data
        num_players_data = [[max(min(elem['num_players_{}'.format(key)],50),0) for elem in two_hours] for key in self.keys]
        return num_players_data

class LineChartNumPlrsPred(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        two_hours = [str(elem['pub_date'])[10:19] for elem in two_hours]
        return two_hours

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""
        data = list(IgnitionRowPredictionOLS.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1]
        num_players_data = [[elem['num_players_{}'.format(key)] for elem in two_hours] for key in self.keys]
        return num_players_data

class LineChartNumPlrsPredCVX(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        two_hours = [str(elem['pub_date'])[10:19] for elem in two_hours]
        return two_hours

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""
        data = list(IgnitionRowPredictionCVX.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1]
        num_players_data = [[elem['num_players_{}'.format(key)] for elem in two_hours] for key in self.keys]
        return num_players_data

class LineChartAvgPot(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        two_hours = [str(elem['pub_date'])[10:19] for elem in two_hours]
        return two_hours

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1] # The most recent two hours of data
        avg_pot_data = [[float(elem['avg_pot_{}'.format(key)]) / (int(key) / 100) for elem in two_hours] 
        	for key in self.keys]
        avg_pot_data = [[max(min(elem, 100),0) for elem in arr] for arr in avg_pot_data] # Assume a max pot size of 2000 BBs
        return avg_pot_data

class LineChartPctFlop(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        two_hours = [str(elem['pub_date'])[10:19] for elem in two_hours]
        return two_hours

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1]
        pct_flop_data = [[int(elem['pct_flop_{}'.format(key)]) for elem in two_hours] 
        	for key in self.keys]
        pct_flop_data = [[min(elem, 100) for elem in arr] for arr in pct_flop_data] # Assume a max pot size of 2000 BBs
        return pct_flop_data


line_chart = TemplateView.as_view(template_name='line_chart.html')
avg_pot_line_chart = TemplateView.as_view(template_name='line_chart_avg_pot.html')
pct_flop_line_chart = TemplateView.as_view(template_name='line_chart_pct_flop.html')
line_chart_json = LineChartJSONView.as_view()
line_chart_avg_pot_json = LineChartAvgPot.as_view()
line_chart_pct_flop_json = LineChartPctFlop.as_view()
line_chart_num_plrs_pred_json = LineChartNumPlrsPred.as_view()
line_chart_num_plrs_pred_cvx_json = LineChartNumPlrsPredCVX.as_view()

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm	

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            return HttpResponseRedirect('goob')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        form = MyModelForm()

    return render(request, 'name.html', {'form': form})

from django.views import generic
from .models import Post

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
