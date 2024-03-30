import json
from django.db import models
from authentication.models import User

class Game(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.TextField()
    Rules = models.TextField()

    def __str__(self):
        return self.Name

class game_matrix(models.Model):
    game_code = models.CharField(max_length=6)
    matrix_map = models.CharField(max_length=50, default="[1,2,3,4,5,6,7,8,9]")

    def get_map(self):
        return json.loads(self.matrix_map)

class game_room(models.Model):
    Player1 = models.ForeignKey(User, on_delete=models.CASCADE)
    Player2 = models.CharField(max_length=100)
    GameName = models.CharField(max_length=100)
    game_code = models.CharField(max_length=6)
    game_matrix = models.ForeignKey(game_matrix, on_delete=models.CASCADE)
