# Generated by Django 3.1 on 2020-10-13 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ignition', '0005_mymodel_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnitionRowPredictionCVX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_players_5', models.IntegerField(default=-1)),
                ('num_players_25', models.IntegerField(default=-1)),
                ('num_players_50', models.IntegerField(default=-1)),
                ('num_players_200', models.IntegerField(default=-1)),
                ('num_players_500', models.IntegerField(default=-1)),
                ('avg_pot_5', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_25', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_50', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_200', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_500', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('pct_flop_5', models.IntegerField(default=-1)),
                ('pct_flop_25', models.IntegerField(default=-1)),
                ('pct_flop_50', models.IntegerField(default=-1)),
                ('pct_flop_200', models.IntegerField(default=-1)),
                ('pct_flop_500', models.IntegerField(default=-1)),
                ('pub_date', models.DateTimeField(verbose_name='published date')),
            ],
        ),
        migrations.CreateModel(
            name='IgnitionRowPredictionOLS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_players_5', models.IntegerField(default=-1)),
                ('num_players_25', models.IntegerField(default=-1)),
                ('num_players_50', models.IntegerField(default=-1)),
                ('num_players_200', models.IntegerField(default=-1)),
                ('num_players_500', models.IntegerField(default=-1)),
                ('avg_pot_5', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_25', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_50', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_200', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('avg_pot_500', models.DecimalField(decimal_places=2, default=-1, max_digits=6)),
                ('pct_flop_5', models.IntegerField(default=-1)),
                ('pct_flop_25', models.IntegerField(default=-1)),
                ('pct_flop_50', models.IntegerField(default=-1)),
                ('pct_flop_200', models.IntegerField(default=-1)),
                ('pct_flop_500', models.IntegerField(default=-1)),
                ('pub_date', models.DateTimeField(verbose_name='published date')),
            ],
        ),
    ]
