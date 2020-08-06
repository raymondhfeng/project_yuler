from django.contrib import admin

from .models import Post 

# Register your models here.

from .models import IgnitionRow

class IgnitionRowAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'num_players_5', 'num_players_25', 'num_players_50', 'num_players_200', 'num_players_500')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
  
admin.site.register(Post, PostAdmin)

admin.site.register(IgnitionRow, IgnitionRowAdmin)