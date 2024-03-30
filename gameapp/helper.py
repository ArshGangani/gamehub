from datetime import timezone
from channels.db import database_sync_to_async
from authentication.models import Chat
from django.contrib.auth.models import User
from authentication.models import ProfileStat
from .models import game_room, game_matrix
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import transaction
import json
@database_sync_to_async
def savetodb(sender_username, receiver_username, message):
    try:
        # Fetch sender and receiver User instances from usernames
        sender_user = User.objects.get(username=sender_username)
        receiver_user = User.objects.get(username=receiver_username)

        # Create a new Chat instance and set its attributes
        chat = Chat(Sender=sender_user, Receiver=receiver_user, Message=message)
        chat.save()
    except Exception as e:
        # Handle exceptions gracefully
        print(f"Error saving to database: {e}")

from channels.db import database_sync_to_async

@database_sync_to_async
def saveStat(game_code, result, player_name):
    try:
        with transaction.atomic():
            game_room_obj = game_room.objects.get(game_code=game_code)
            player1 = User.objects.get(username=game_room_obj.Player1)
            player2 = User.objects.get(username=game_room_obj.Player2)

            player1_profile = ProfileStat.objects.get(Name=player1)
            player2_profile = ProfileStat.objects.get(Name=player2)

            player1_profile.No_of_games_played += 1
            player2_profile.No_of_games_played += 1

            if not result:
                player1_profile.No_of_game_draw += 1
                player2_profile.No_of_game_draw += 1
            else:
                if player1_profile.Name.username == player_name:
                    player1_profile.No_of_game_won += 1
                else:
                    player2_profile.No_of_game_won += 1
            player1_profile.save()
            player2_profile.save()
    except (game_room.DoesNotExist, User.DoesNotExist, ProfileStat.DoesNotExist):
        # Handle cases where game room, user, or profile stat does not exist
        pass

@database_sync_to_async
def setup_game(game_code, game_matrix_id, player_name, player_type):
    # Retrieve the User instance corresponding to the player's name
    player1 = User.objects.get(username=player_name)

    # Retrieve the game_matrix_instance
    game_matrix_instance = game_matrix.objects.get(id=game_matrix_id)    

    if player_type == 'null':
        game = game_room.objects.get(game_code=game_code, Player1=player1, game_matrix=game_matrix_instance)
        return game.id

    elif player_type == 'on':
        game = game_room.objects.filter(game_code=game_code).first()
        if game:
            game.Player2 = player_name  # Fix typo here from game.game_opponent to game.Player2
            game.save()
        return game.id if game else None

@database_sync_to_async
def update_matrix(matrix_id, box_id, player_type):
    print(matrix_id + " matrixid")
    print(box_id + " box_id")
    print(player_type + "player_type ")
    game_matrix_map = game_matrix.objects.get(id=matrix_id).get_map()
    box_id = int(box_id) - 1

    if(player_type == 'null'):
        game_matrix_map[box_id] = 44
    elif(player_type == 'on'):
        game_matrix_map[box_id] = 11

    updated_matrix_map = json.dumps(game_matrix_map)
    game_matrix.objects.filter(id=matrix_id).update(matrix_map=updated_matrix_map)

@database_sync_to_async
def check_winner(matrix_id):

    base_map = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    gm_map = game_matrix.objects.get(id=matrix_id).get_map()
    
    if( (gm_map[0] == gm_map[1] == gm_map[2] == 11) or (gm_map[3] == gm_map[4] == gm_map[5] == 11) or (gm_map[6] == gm_map[7] == gm_map[8] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[1] == gm_map[2] == 44) or (gm_map[3] == gm_map[4] == gm_map[5] == 44) or (gm_map[6] == gm_map[7] == gm_map[8] == 44) ): 
        return 44
    elif( (gm_map[0] == gm_map[3] == gm_map[6] == 11) or (gm_map[1] == gm_map[4] == gm_map[7] == 11) or (gm_map[2] == gm_map[5] == gm_map[8] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[3] == gm_map[6] == 44) or (gm_map[1] == gm_map[4] == gm_map[7] == 44) or (gm_map[2] == gm_map[5] == gm_map[8] == 44) ):
        return 44
    elif( (gm_map[0] == gm_map[4] == gm_map[8] == 11) or (gm_map[2] == gm_map[4] == gm_map[6] == 11) ):
        return 11
    elif( (gm_map[0] == gm_map[4] == gm_map[8] == 44) or (gm_map[2] == gm_map[4] == gm_map[6] == 44) ):
        return 44
    else:
        return any(element in gm_map for element in base_map)