from __future__ import absolute_import, unicode_literals
from celery import task

from ignition.models import IgnitionRow
from django.utils import timezone

import sys
# sys.path.insert(1, '/Users/raymondfeng/Desktop/TrickyWays/cropped') # TODO: Make this configurable
sys.path.insert(1,'/home/pi/project_genovese')
sys.path.insert(1,'/home/pi/django-tutorial/ignition')

from get_ignition_stats_windows import get_stats

import requests
import json
import base64
import os

from datetime import datetime

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
