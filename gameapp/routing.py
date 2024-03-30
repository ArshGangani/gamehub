#chat
from django.urls import path , include
from gameapp.consumers import PostConsumer
from gameapp.consumers import GameConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
	path("" , PostConsumer.as_asgi()) ,
    path('ws/asc/pg/<str:game_code>/<str:game_matrix_id>/<str:player_name>/<str:player_type>/', GameConsumer.as_asgi())
]
