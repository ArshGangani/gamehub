from django.contrib import admin
from .models import game_matrix, Game, game_room
# Register your models here.

admin.site.register(Game)
admin.site.register(game_room)
admin.site.register(game_matrix)
