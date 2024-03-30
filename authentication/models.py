from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    Sender = models.ForeignKey(User,on_delete = models.CASCADE,related_name='sent_chats')
    Receiver = models.ForeignKey(User,on_delete = models.CASCADE,related_name='received_chats')
    Message = models.TextField()

class ProfileStat(models.Model):
    Name = models.ForeignKey(User,on_delete=models.CASCADE)
    No_of_games_played = models.BigIntegerField(default=0)
    No_of_game_won = models.BigIntegerField(default=0)
    No_of_game_draw = models.BigIntegerField(default=0)



