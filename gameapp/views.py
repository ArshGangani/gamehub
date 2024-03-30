from django.shortcuts import render
from flask import redirect
from gameapp.forms import GameSelectionForm
from gameapp.models import game_matrix, game_room
from authentication.models import ProfileStat
from django.contrib.auth.models import User

# Assuming game_matrix_id is the correct foreign key field in game_room model

def room(request):
    current_user = request.user
    if request.method == 'POST':
        form = GameSelectionForm(request.POST, current_user=current_user)
        if form.is_valid():
            selected_game = form.cleaned_data['game']
            opponent = form.cleaned_data['Opponent']
            game_code = form.cleaned_data['game_code']
            provided_gamecode = game_code
            player1 = request.user
            
            # Create and save game_matrix object
            game_room1 = {}
            if not form.cleaned_data['have_code']:
                # Create new game_room object
                game_matrix_object = game_matrix.objects.create(game_code=provided_gamecode)
                game_matrix_object_id = game_matrix_object.id
                game_room_obj = game_room.objects.create(Player1=player1, Player2=opponent,
                                                         GameName=selected_game.Name,game_code=game_code, game_matrix_id=game_matrix_object.id)
                existing_game_room = game_room.objects.filter(game_code=provided_gamecode).first()
                game_room1 = {
                    "player1": player1,
                    "player2": opponent,
                    "game_code": game_code,  # Include game code in the dictionary
                    "game_matrix_id":game_matrix_object_id,
                    "have_code": "null"
                }
                if not existing_game_room:
                    game_room_obj.save()
            else:
                # Retrieve existing game_room object
                game_matrix_object = game_matrix.objects.get(game_code=provided_gamecode)
                game_matrix_object_id = game_matrix_object.id
                game_room_obj = game_room.objects.get(game_code=provided_gamecode)
                if str(request.user) != str(game_room_obj.Player2):
                    form = GameSelectionForm(current_user=current_user)
                    return render(request, 'game_selection.html', {'form': form})
                
                player1_name = game_room_obj.Player1.username
                player2_name = game_room_obj.Player2
                game_room1 = {
                    "player1": player1_name,
                    "player2": player2_name,
                    "game_code": game_code,  # Include game code in the dictionary
                    "game_matrix_id":game_matrix_object_id,
                    "have_code": "on"
                }
            return render(request, 'game_room.html', {'game_room': game_room1})
    else:
        form = GameSelectionForm(current_user=current_user)
    return render(request, 'game_selection.html', {'form': form})


def game_room_view(request, gamecode):
    return render(request, 'game_room.html', {'gamecode': gamecode})


def profile_stats(request, username):
    user = User.objects.get(username=username)
    profile = ProfileStat.objects.get(Name=user)
    games_defeated = profile.No_of_games_played - profile.No_of_game_won - profile.No_of_game_draw

    return render(request, 'profile_stats.html', {'profile': profile,'games_defeated': games_defeated})