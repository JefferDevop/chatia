# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WhatsAppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "whatsapp_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("WebSocket conectado.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("WebSocket desconectado.")

    async def receive(self, text_data):
        # Si quieres aceptar mensajes desde el frontend (opcional)
        print("Mensaje recibido en WebSocket:", text_data)

    async def send_whatsapp_event(self, event):
        await self.send(text_data=json.dumps(event["data"]))

        

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


