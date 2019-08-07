from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        # Somente caracteres ASCII para o nome grupo
        self.room_group_name = 'chat_%s' % self.room_name

        # Junte-se ao grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Deixe o grupo da sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Desconectou...")
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    #Receber mensagem do grupo de salas
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
    