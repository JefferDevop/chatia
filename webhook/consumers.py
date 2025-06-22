# app_whatsapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import WhatsAppMessage  # Asegúrate de que sea tu modelo correcto

class WhatsAppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.wa_id = self.scope['url_route']['kwargs']['wa_id']
        self.room_group_name = f'chat_{self.wa_id}'

        # Unirse al grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Enviar historial al conectar
        mensajes = await sync_to_async(self.get_mensajes)()
        await self.send(text_data=json.dumps({
            "event": "historial",
            "mensajes": mensajes
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Aquí podrías manejar mensajes enviados desde el frontend (opcional)
        pass

    async def send_whatsapp_event(self, event):
        # Enviar evento desde backend al frontend
        await self.send(text_data=json.dumps(event["data"]))

    def get_mensajes(self):
        mensajes = WhatsAppMessage.objects.filter(
            wa_id=self.wa_id
        ).order_by('-wa_timestamp')[:20]

        return [
            {
                "sender_name": m.sender_name,
                "body": m.message_body,
                "timestamp": m.wa_timestamp.isoformat(),
                "message_type": m.message_type,
                "id": m.message_id
            } for m in mensajes[::-1]
        ]

        

# # app_whatsapp/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class WhatsAppConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'whatsapp_updates'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({"status": "connected"}))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         pass  # No recibimos datos del front

#     async def send_whatsapp_message(self, event):
#         await self.send(text_data=json.dumps(event["message"]))


