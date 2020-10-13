from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from ignition.models import IgnitionRow

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
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = data[::-1]
        data = pd.DataFrame(two_hours)
        data['pub_date'] = data.apply(lambda x: str(x['pub_date']),axis=1)
        data['pub_date_struct'] = data.apply(lambda x: time.strptime(x['pub_date'],"%Y-%m-%d %H:%M:%S.%f%z"),axis=1)
        data.index = data.apply(lambda x: datetime.fromtimestamp(mktime(x['pub_date_struct'])),axis=1)
        data['hour'] = data.apply(lambda x: str(time.strptime(x['pub_date'],"%Y-%m-%d %H:%M:%S.%f%z")[3]), axis=1)
        data['day_of_week'] = data.index.map(lambda x: x.weekday())
        data['hour'] = pd.Categorical(
            data['hour'], categories=list(range(24)))
        data['day_of_week'] = pd.Categorical(
            data['day_of_week'], categories=list(range(7)))
        hour_dummies = pd.get_dummies(data['hour'], drop_first=True)
        hour_dummies.columns = ['h'+ str(elem) for elem in hour_dummies.columns]
        day_of_week_dummies = pd.get_dummies(data['day_of_week'], drop_first=True)
        day_of_week_dummies.columns = ['dow'+str(elem) for elem in day_of_week_dummies.columns]
        data = pd.concat((data,hour_dummies,day_of_week_dummies), axis=1)
        results5 = OLSResults.load("ols_9_21_data_5.pickle")
        results25 = OLSResults.load("ols_9_21_data_25.pickle")
        results50 = OLSResults.load("ols_9_21_data_50.pickle")
        results200 = OLSResults.load("ols_9_21_data_200.pickle")
        results500 = OLSResults.load("ols_9_21_data_500.pickle")
        preds5 = results5.predict(data)
        preds25 = results25.predict(data)
        preds50 = results50.predict(data)
        preds200 = results200.predict(data)
        preds500 = results500.predict(data)
        preds = [preds5,preds25,preds50,preds200,preds500]
        return [[int(elem) for elem in pred.values] for pred in preds]

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
        data = list(IgnitionRow.objects.all().order_by('-pub_date')[:self.num_ticks].values())
        two_hours = reversed(data)
        data = pd.DataFrame(two_hours)
        data['pub_date'] = data.apply(lambda x: str(x['pub_date']),axis=1)
        data['pub_date_struct'] = data.apply(lambda x: time.strptime(x['pub_date'],"%Y-%m-%d %H:%M:%S.%f%z"),axis=1)
        data.index = data.apply(lambda x: datetime.fromtimestamp(mktime(x['pub_date_struct'])),axis=1)
        data['hour'] = data.apply(lambda x: str(time.strptime(x['pub_date'],"%Y-%m-%d %H:%M:%S.%f%z")[3]), axis=1)
        data['day_of_week'] = data.index.map(lambda x: x.weekday())
        data['hour'] = pd.Categorical(
            data['hour'], categories=list(range(24)))
        data['day_of_week'] = pd.Categorical(
            data['day_of_week'], categories=list(range(7)))
        hour_dummies = pd.get_dummies(data['hour'], drop_first=True)
        hour_dummies.columns = ['h'+ str(elem) for elem in hour_dummies.columns]
        day_of_week_dummies = pd.get_dummies(data['day_of_week'], drop_first=True)
        day_of_week_dummies.columns = ['dow'+str(elem) for elem in day_of_week_dummies.columns]
        cols_keep = ['num_players_5','num_players_25','num_players_50','num_players_200','num_players_500']
        data = data[cols_keep]
        data = pd.concat((data,hour_dummies,day_of_week_dummies), axis=1)

        all_models =  ['cvxpy_constraint_num_plrs_5.txt','cvxpy_constraint_num_plrs_25.txt',
        'cvxpy_constraint_num_plrs_50.txt','cvxpy_constraint_num_plrs_200.txt','cvxpy_constraint_num_plrs_500.txt']
        all_preds = []

        for i in range(len(all_models)):
            this_data = data.drop(labels=cols_keep[i],axis=1)
            this_data = np.array(this_data.values)
            c_cvx = np.loadtxt(all_models[i], dtype=float)
            preds = this_data @ c_cvx
            preds = list(preds)
            all_preds.append(preds)


        return all_preds


class LineChartAvgPot(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500','Avg']

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

        data = list(IgnitionRow.objects.all().order_by('pub_date').values())
        two_hours = data[-self.num_ticks:] # The most recent two hours of data
        avg_pot_data = [[float(elem['avg_pot_{}'.format(key)]) / (int(key) / 100) for elem in two_hours] 
        	for key in self.keys[:-1]]
        avg_pot_data = [[max(min(elem, 100),0) for elem in arr] for arr in avg_pot_data] # Assume a max pot size of 2000 BBs
        average = sum([np.array(lst) for lst in avg_pot_data]) / 5
        avg_pot_data.append(list(average))
        return avg_pot_data

class LineChartPctFlop(BaseLineChartView):

    def __init__(self):
        self.num_ticks = NUM_TICKS
        self.keys = ['5','25','50','200','500', 'Avg']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return ["January", "February", "March", "April", "May", "June", "July"]
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
        	for key in self.keys[:-1]]
        pct_flop_data = [[min(elem, 100) for elem in arr] for arr in pct_flop_data] # Assume a max pot size of 2000 BBs
        average = sum([np.array(lst) for lst in pct_flop_data]) / 5
        pct_flop_data.append(list(average))
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
