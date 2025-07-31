from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import WhatsAppMessage


class WhatsAppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.wa_id = self.scope['url_route']['kwargs'].get('wa_id')

        if not self.wa_id:
            await self.close(code=4001)  # Código personalizado: wa_id no proporcionado
            return

        self.room_group_name = f'chat_{self.wa_id}'

        # Unirse al grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Enviar historial al conectar
        try:
            mensajes = await sync_to_async(self.get_mensajes)()
            await self.send(text_data=json.dumps({
                "event": "historial",
                "mensajes": mensajes
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "event": "error",
                "message": "Error al obtener historial",
                "error": str(e)
            }))

    async def disconnect(self, close_code):
        # Salir del grupo al desconectar
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            evento = data.get("event")

            if evento == "marcar_leido":
                message_id = data.get("message_id")
                if message_id:
                    await sync_to_async(self.marcar_mensaje_leido)(message_id)
                    await self.send(text_data=json.dumps({
                        "event": "mensaje_leido",
                        "message_id": message_id
                    }))

            elif evento == "marcar_conversacion_leida":
                await sync_to_async(self.marcar_conversacion_leida)()
                await self.send(text_data=json.dumps({
                    "event": "conversacion_marcada_leida"
                }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                "event": "error",
                "message": "Error en el mensaje recibido",
                "error": str(e)
            }))

    def get_mensajes(self):
        mensajes = WhatsAppMessage.objects.filter(
            conversacion__cliente__wa_id=self.wa_id
        ).order_by('-timestamp')[:20]

        return [
            {
                "sender_name": m.conversacion.cliente.nombre,
                "body": m.mensaje,
                "timestamp": m.timestamp.isoformat(),
                "message_type": m.tipo,
                "id": m.message_id
            } for m in reversed(mensajes)
        ]

    def marcar_conversacion_leida(self):
        WhatsAppMessage.objects.filter(
            conversacion__cliente__wa_id=self.wa_id,
            tipo='entrante',
            visto=False
        ).update(visto=True)

    def marcar_mensaje_leido(self, message_id):
        try:
            mensaje = WhatsAppMessage.objects.get(message_id=message_id)
            mensaje.visto = True
            mensaje.save()
        except WhatsAppMessage.DoesNotExist:
            pass  # Silenciar si el mensaje no existe

    async def send_whatsapp_event(self, event):
        # Método para enviar datos desde backend al frontend vía WebSocket
        await self.send(text_data=json.dumps(event["data"]))






# app_whatsapp/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from asgiref.sync import sync_to_async
# from .models import WhatsAppMessage  # Asegúrate de que sea tu modelo correcto

# class WhatsAppConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.wa_id = self.scope['url_route']['kwargs']['wa_id']
#         self.room_group_name = f'chat_{self.wa_id}'

#         # Unirse al grupo
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#         # Enviar historial al conectar
#         mensajes = await sync_to_async(self.get_mensajes)()
#         await self.send(text_data=json.dumps({
#             "event": "historial",
#             "mensajes": mensajes
#         }))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)



#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         evento = data.get("event")

#         if evento == "marcar_leido":
#             message_id = data.get("message_id")
#             if message_id:
#                 await sync_to_async(self.marcar_mensaje_leido)(message_id)

#         elif evento == "marcar_conversacion_leida":
#             await sync_to_async(self.marcar_conversacion_leida)()


#     def marcar_conversacion_leida(self):
#         mensajes = WhatsAppMessage.objects.filter(
#             conversacion__cliente__wa_id=self.wa_id,
#             tipo='entrante',
#             visto=False
#         )
#         for m in mensajes:
#             m.visto = True
#             m.save()


#     async def send_whatsapp_event(self, event):
#         # Enviar evento desde backend al frontend
#         await self.send(text_data=json.dumps(event["data"]))

#     def get_mensajes(self):
#         mensajes = WhatsAppMessage.objects.filter(
#             conversacion__cliente__wa_id=self.wa_id
#         ).order_by('-timestamp')[:20]

#         return [
#             {
#                 "sender_name": m.conversacion.cliente.nombre,
#                 "body": m.mensaje,
#                 "timestamp": m.timestamp.isoformat(),
#                 "message_type": m.tipo,
#                 "id": m.message_id
#             } for m in reversed(mensajes)
#         ]


        

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


