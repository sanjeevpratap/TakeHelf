from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from .models import CustomUser,Message
from .models import Thread


class EchoConsumer(SyncConsumer):
    print("hheleelejlelr i am be")
    def websocket_connect(self, event):
        self.room_name = 'broadcast'
        print('websocket Connected...', event)
        print('ssssChannel layer..', self.channel_layer)  # get default channel layer from a project
        print('Channel name..', self.channel_name)  # get default channel name from a project
        me=self.scope['user']
        other_username=self.scope['url_route']['kwargs']['username']
        other_user=CustomUser.objects.get(username=other_username)
        print(other_user)
        thread_obj=Thread.objects.get_or_create_personal_thread(me,other_user)
        print(thread_obj,me,"    ",other_user)
        self.room_name = f'personal_thread_{thread_obj.id}'
        # self.room_name ='personal_thread_41'
        print(self.room_name,",,,,,,,,,,,,,,,,,,,,,,,")
        self.send({
            'type': 'websocket.accept'
        })

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'[{self.channel_name}]- you are connected')

    def websocket_receive(self, event):
        # print(f'[{self.channel_name}]- you are received - {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(       
            self.room_name,
            # self.channel_name,
            {
                 'type':'chat.message',
                 'text':event.get('text')
            }
           )
        sender = self.scope['user']
        me=self.scope['user']
        other_username=self.scope['url_route']['kwargs']['username']
        other_user=CustomUser.objects.get(username=other_username)
        thread_obj=Thread.objects.get_or_create_personal_thread(me,other_user)
        text = event.get('text')
        message = Message.objects.create(sender=sender, thread=thread_obj, text=text)
        print(f'Message saved in the database: {message}')

    def chat_message(self, event):
        # print(f'[{self.channel_name}]- message sent - {event["text"]}')

        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self, event):
        # print(f'[{self.channel_name}]- Disconnected')

        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        print("connection is disconnected")
        print(event)