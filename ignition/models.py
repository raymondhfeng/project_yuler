from django.db import models
# from django.utils import timezone
# import datetime

# Create your models here.

class IgnitionRow(models.Model):
	num_players_5 = models.IntegerField(default=-1)
	num_players_25 = models.IntegerField(default=-1)
	num_players_50 = models.IntegerField(default=-1)
	num_players_200 = models.IntegerField(default=-1)
	num_players_500 = models.IntegerField(default=-1)
	avg_pot_5 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
	avg_pot_25 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
	avg_pot_50 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
	avg_pot_200 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
	avg_pot_500 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
	pub_date = models.DateTimeField('published date')