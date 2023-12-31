from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from . import consumers

# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         path('ws/chat/',EchoConsumer)
#     ])
# })
print(".............................")
websocket_urlpatterns=[
    # print("..........................................."),
    # path('ws/chat/<str:username>',consumers.ChatConsumer.as_asgi()),
    # path('',consumers.EchoConsumer.as_asgi()),
    path('ws/chat/<str:username>/',consumers.EchoConsumer.as_asgi()),
    # path('ws/chat/',consumers.EchoConsumer.as_asgi()),
]