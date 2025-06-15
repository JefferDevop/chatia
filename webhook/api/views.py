from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import WhatsAppMessage, MessageStatus
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if mode == "subscribe" and token == "demo":
            return JsonResponse({'hub.challenge': challenge})
        return JsonResponse({}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            entry = data['entry'][0]
            change = entry['changes'][0]
            value = change['value']
            messaging_product = value.get("messaging_product")

            # Procesar mensajes entrantes
            if 'messages' in value:
                message = value['messages'][0]
                wa_id = message['from']
                body = message.get('text', {}).get('body', '')
                sender_name = value['contacts'][0]['profile']['name']
                timestamp = message['timestamp']

                msg = WhatsAppMessage.objects.create(
                    wa_id=wa_id,
                    sender_name=sender_name,
                    message_body=body,
                    wa_timestamp=timestamp,
                )

                # Emitir a WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "whatsapp_group",
                    {
                        "type": "new.whatsapp.message",
                        "message": {
                            "type": "incoming",
                            "id": msg.id,
                            "from": wa_id,
                            "sender_name": sender_name,
                            "body": body,
                            "timestamp": timestamp
                        }
                    }
                )

            # Procesar estados: delivered, read, etc.
            elif 'statuses' in value:
                status = value['statuses'][0]
                msg_id = status['id']
                status_type = status['status']
                recipient_id = status.get('recipient_id')
                timestamp = status.get('timestamp')

                # Guarda o actualiza el estado
                MessageStatus.objects.create(
                    message_id=msg_id,
                    status=status_type,
                    recipient_id=recipient_id,
                    wa_timestamp=timestamp
                )

                # Emitir estado por WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "whatsapp_group",
                    {
                        "type": "new.whatsapp.message",
                        "message": {
                            "type": "status",
                            "message_id": msg_id,
                            "status": status_type,
                            "timestamp": timestamp,
                            "recipient": recipient_id
                        }
                    }
                )

            return JsonResponse({'status': 'received'}, status=200)

        except Exception as e:
            print("Error al procesar:", e)
            return JsonResponse({'error': 'Formato no válido'}, status=400)





# # app_whatsapp/views.py
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from ..models import WhatsAppMessage
# import json

# @csrf_exempt
# def whatsapp_webhook(request):
#     if request.method == 'GET':
#         mode = request.GET.get('hub.mode')
#         token = request.GET.get('hub.verify_token')
#         challenge = request.GET.get('hub.challenge')
#         if mode == 'subscribe' and token == 'demo':
#             return HttpResponse(challenge, status=200)
#         return HttpResponse("Forbidden", status=403)

#     if request.method == 'POST':
#         data = json.loads(request.body)

#         print("Datos recibidos:", data)

#         # Extrae datos del mensaje (ajusta esto según el payload real)
#         try:
#             entry = data['entry'][0]
#             change = entry['changes'][0]
#             message_data = change['value']['messages'][0]
#             wa_id = message_data['from']
#             body = message_data['text']['body']
#             sender_name = change['value']['contacts'][0]['profile']['name']
#         except Exception as e:
#             print("Error al procesar:", e)
#             return JsonResponse({'error': 'Formato no válido'}, status=400)

#         # Guarda en la base de datos
#         msg = WhatsAppMessage.objects.create(
#             wa_id=wa_id,
#             sender_name=sender_name,
#             message_body=body
#         )

#         # Enviar por Django Channels
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'whatsapp_updates',
#             {
#                 'type': 'send_whatsapp_message',
#                 'message': {
#                     'wa_id': wa_id,
#                     'sender_name': sender_name,
#                     'body': body,
#                     'timestamp': str(msg.timestamp)
#                 }
#             }
#         )

#         return JsonResponse({'status': 'received'}, status=200)
