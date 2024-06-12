from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from SmfAttendance import shortcuts
from channels.exceptions import DenyConnection
from django.shortcuts import get_object_or_404
from accounts import models as account_models
from session import models as session_models
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer

class SessionConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.channel_layer: RedisChannelLayer = get_channel_layer()
        super().__init__(*args, **kwargs)

    def connect(self):

        session_pk = self.scope.get('url_route').get('kwargs').get('pk')
        session = get_object_or_404(session_models.Session, id=session_pk)

        if not self.scope.get('user'):
            raise DenyConnection
        
        user_pk = self.scope.get('user').get('user_id')
        admin = get_object_or_404(account_models.Admin, id=user_pk)

        is_session_owner = shortcuts.sessionOwner(session_pk=session_pk, user_pk=user_pk)

        if not is_session_owner:
            raise DenyConnection
        
        self.group_name = session.name
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def session_update(self, event):
        self.send(text_data=event['data'])
    
