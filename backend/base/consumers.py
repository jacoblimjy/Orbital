import json
from channels.generic.websocket import WebsocketConsumer
from base.models import Ingredient
from base.serializers import IngredientSerializer, UserSerializer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'notifications_' + str(self.scope["user_id"])
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'Hello World!'
        }))
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        data = Ingredient.objects.all()
        # serializer = IngredientSerializer(data, many=True)
        
        user = get_user_model().objects.get(id=self.scope["user_id"])
        serializer = UserSerializer(user)

        self.send(text_data=json.dumps({
            'data': serializer.data
        }))

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': "notification",
            'message': message
        }))
    
