

# import os
# import twapp.routing
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetme.settings')

# # application = get_asgi_application()
# print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket':AuthMiddlewareStack(
#         URLRouter(
            
#         twapp.routing.websocket_urlpatterns
#     )
#     )

# })


import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import twapp.routing  # Make sure this import is correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweetme.settings')
print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            twapp.routing.websocket_urlpatterns
        )
    ),
})

