from django.contrib import admin

# Register your models here.

from .models import IgnitionRow

class IgnitionRowAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'num_players_5', 'num_players_25', 'num_players_50', 'num_players_200', 'num_players_500')

admin.site.register(IgnitionRow, IgnitionRowAdmin)