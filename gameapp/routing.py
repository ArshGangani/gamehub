from django.urls import path , include
from gameapp.consumers import PostConsumer
from gameapp.consumers import GameConsumer

websocket_urlpatterns = [
	path("" , PostConsumer.as_asgi()) ,
    path('ws/asc/pg/<str:game_code>/<str:game_matrix_id>/<str:player_name>/<str:player_type>/', GameConsumer.as_asgi())
]
