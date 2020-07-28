from __future__ import absolute_import, unicode_literals
from celery import task

from ignition.models import IgnitionRow
from django.utils import timezone

import sys
sys.path.insert(1, '/Users/raymondfeng/Desktop/TrickyWays/cropped')

from get_ignition_stats import get_stats

@task()
def task_number_one():

	num_ppl, avg_pot, plrs_flop = get_stats()
	num_ppl = [elem if elem != '' else '-1' for elem in num_ppl]
	num_ppl = [int(elem.replace('+','')) for elem in num_ppl]
	avg_pot = [elem if elem != '' else '-1' for elem in avg_pot]
	avg_pot = [float(elem.replace('$','').strip('.')) for elem in avg_pot]
	pct_flop = [elem if elem != '' else '-1' for elem in plrs_flop]
	pct_flop = [int(elem.replace('%','')) for elem in pct_flop]
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