import os
from django.core.asgi import get_asgi_application


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
import gameapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')

application = ProtocolTypeRouter(
	{
		"http" : get_asgi_application() , 
		"websocket" : AuthMiddlewareStack(
			URLRouter(
				gameapp.routing.websocket_urlpatterns
			) 
		)
	}
)