from __future__ import absolute_import, unicode_literals
from celery import task

from ignition.models import IgnitionRow,IgnitionRowPredictionOLS,IgnitionRowPredictionCVX
from django.utils import timezone

import sys
sys.path.insert(1,'/home/pi/project_yuler/ignition')

from get_ignition_stats_windows import get_stats

import requests
import pandas as pd
import json
import base64
import os
import glob

import numpy as np
import statsmodels.formula.api as sm
import time
from datetime import datetime, timedelta
from time import mktime
from statsmodels.regression.linear_model import OLSResults

from PIL import Image


@task()
def task_number_one():
        num_ppl, avg_pot, plrs_flop = get_stats()
        for i in range(len(num_ppl)):
                num_ppl[i] = num_ppl[i].replace('+','')
                try:
                        num_ppl[i] = int(num_ppl[i])
                except ValueError:
                        num_ppl[i] = -1
        for i in range(len(avg_pot)):
                avg_pot[i] = avg_pot[i].replace('$','').strip('.')
                try:
                        avg_pot[i] = float(avg_pot[i])
                except ValueError:
                        avg_pot[i] = -1
        for i in range(len(plrs_flop)):
                plrs_flop[i] = plrs_flop[i].replace('%','')
                plrs_flop[i] = plrs_flop[i][:2] # TODO: This is clunky
                try:
                        plrs_flop[i] = int(plrs_flop[i])
                except ValueError:
                        plrs_flop[i] = -1
        pct_flop = plrs_flop    
        d = IgnitionRow(num_players_5=num_ppl[0],
                                        num_players_25=num_ppl[1],
                                        num_players_50=num_ppl[2],
                                        num_players_200=num_ppl[3],
                                        num_players_500=num_ppl[4],
                                        avg_pot_5=avg_pot[0],
                                        avg_pot_25=avg_pot[1],
                                        avg_pot_50=avg_pot[2],
                                        avg_pot_200=avg_pot[3],
                                        avg_pot_500=avg_pot[4],
                                        pct_flop_5=pct_flop[0],
                                        pct_flop_25=pct_flop[1],
                                        pct_flop_50=pct_flop[2],
                                        pct_flop_200=pct_flop[3],
                                        pct_flop_500=pct_flop[4],
                                        pub_date=timezone.now())
      
        
        d.save()

        def storeOLSPrediction():
            data = list(IgnitionRow.objects.all().order_by('-pub_date')[:1].values())
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
            results5 = OLSResults.load("regression_models/ols_9_21_data_5.pickle")
            results25 = OLSResults.load("regression_models/ols_9_21_data_25.pickle")
            results50 = OLSResults.load("regression_models/ols_9_21_data_50.pickle")
            results200 = OLSResults.load("regression_models/ols_9_21_data_200.pickle")
            results500 = OLSResults.load("regression_models/ols_9_21_data_500.pickle")
            preds5 = results5.predict(data)
            preds25 = results25.predict(data)
            preds50 = results50.predict(data)
            preds200 = results200.predict(data)
            preds500 = results500.predict(data)
            preds = [preds5,preds25,preds50,preds200,preds500]
            print("OLS PREDICTIONS: {}".format(preds))
            d = IgnitionRowPredictionOLS(num_players_5=preds[0],num_players_25=preds[1],num_players_50=preds[2],
                    num_players_200=preds[3],num_players_500=preds[4],pub_date=timezone.now())
            d.save()

        def storeCVXPrediction():
            data = list(IgnitionRow.objects.all().order_by('-pub_date')[:1].values())
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
                c_cvx = np.loadtxt("regression_models/" + all_models[i], dtype=float)
                preds = this_data @ c_cvx
                preds = list(preds)
                all_preds.append(preds)

            preds = all_preds

            d = IgnitionRowPredictionCVX(num_players_5=preds[0][0],num_players_25=preds[1][0],num_players_50=preds[2][0],
                    num_players_200=preds[3][0],num_players_500=preds[4][0],pub_date=timezone.now())
            print("CVX PREDICTIONS: {}".format(preds))
            d.save()

        storeOLSPrediction()
        storeCVXPrediction()

@task()
def task_number_two():
    resp = requests.get('http://2835dba625aa.ngrok.io/ignition_data') # TODO: Make this configurable
    img = json.loads(resp.text)['img']
    img = base64.b64decode(img)

    date_string = str(datetime.now()).replace('-','_').replace(' ', '_').replace(':','_').replace('.', '')

    image_path = os.path.join('/home/pi/screenshots/', date_string + '.jpeg') # TODO: Make this configurable 
    print('saved file: ', image_path)

    with open(image_path, 'wb') as f:
        f.write(img)

@task()
def clean_screenshots():  
    files = glob.glob('/home/pi/screenshots/*')
    for f in files:
        os.remove(f)

@task()
def stitch_photos():
    ax1 = ["num_ppl","avg_pot_fishy","avg_pot","plrs_flop"]
    ax2 = [str(elem) for elem in list(range(5))]

    #creates a new empty image, RGB mode, and size 400 by 400.
    new_im = Image.new('RGB', (500,200))

    #Iterate through a 4 by 4 grid with 100 spacing, to place my image
    for i in range(0,500,100):
        for j in range(0,200,50):
            #opens an image:
            # print(j//50,i//100)
            im = Image.open("/ignition/static/ignition/fishy_ocr/{}.png".format(ax1[j//50]+"_"+ax2[i//100]))
            im.thumbnail((100,100))
            im = Image.eval(im,lambda x: x)
            #paste the image at location i,j:
            new_im.paste(im, (i,j))

    # new_im.show()
    new_im.save("/ignition/static/ignition/fishy_ocr/stitched_fishy_ocrs.png")