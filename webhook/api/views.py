# views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
import pytz
import json
from ..models import WhatsAppMessage, WhatsAppContact, WhatsAppMessageStatus

from ..whatsapp_utils import enviar_mensaje_template


# @method_decorator(csrf_exempt, name='dispatch')
class WhatsAppWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        print("WhatsAppWebhookAPIView cargada")
        print(" Headers:", dict(request.headers))
        print("Query Params:", request.query_params)
        print("GET Params:", request.GET.dict())
        print("Raw Body (GET):", request.body)

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == 'demo':
            return JsonResponse({'hub.challenge': challenge})
        return JsonResponse({}, status=403)

    def post(self, request):
        print(" WhatsAppWebhookAPIView recibido POST")
        print(" Headers:", dict(request.headers))
        print(" Raw Body:", request.body)
        print(" JSON:", request.data)

        try:
            data = request.data
            channel_layer = get_channel_layer()

            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})

                    # Mensaje entrante
                    if 'messages' in value:
                        message_data = value['messages'][0]
                        wa_id = message_data['from']
                        texto = message_data['text']['body']
                        timestamp = message_data['timestamp']
                        sender_name = value['contacts'][0]['profile']['name']

                        # Guardar mensaje
                        WhatsAppMessage.objects.create(
                            wa_id=wa_id,
                            sender_name=sender_name,
                            body=texto,
                            timestamp=timestamp,
                            direction='IN'
                        )

                        # Actualizar contacto
                        contacto, creado = WhatsAppContact.objects.get_or_create(
                            wa_id=wa_id,
                            defaults={"nombre": sender_name}
                        )
                        contacto.last_interaction = datetime.fromtimestamp(int(timestamp), tz=pytz.UTC)
                        contacto.save()

                        # Enviar al frontend
                        async_to_sync(channel_layer.group_send)(
                            "whatsapp_updates",
                            {
                                "type": "send_whatsapp_event",
                                "data": {
                                    "event": "new_message",
                                    "wa_id": wa_id,
                                    "sender_name": sender_name,
                                    "body": texto,
                                    "timestamp": timestamp
                                }
                            }
                        )

                    # \ud83d\udfe1 Estados (delivered, read)
                    elif 'statuses' in value:
                        for status_info in value['statuses']:
                            msg_id = status_info['id']
                            status = status_info['status']
                            raw_timestamp = int(status_info['timestamp'])
                            timestamp = datetime.fromtimestamp(raw_timestamp, tz=pytz.UTC)
                            wa_id = status_info['recipient_id']

                            # Datos opcionales
                            conversation_id = status_info.get('conversation', {}).get('id')
                            category = status_info.get('pricing', {}).get('category')
                            pricing_model = status_info.get('pricing', {}).get('pricing_model')

                            WhatsAppMessageStatus.objects.create(
                                message_id=msg_id,
                                wa_id=wa_id,
                                status=status,
                                timestamp=timestamp,
                                conversation_id=conversation_id,
                                category=category,
                                pricing_model=pricing_model
                            )

                            # \ud83d\udd35 Actualizar contacto si existe
                            try:
                                contacto = WhatsAppContact.objects.get(wa_id=wa_id)
                                contacto.last_interaction = timestamp
                                contacto.save()
                            except WhatsAppContact.DoesNotExist:
                                pass

                            # Enviar al frontend
                            async_to_sync(channel_layer.group_send)(
                                "whatsapp_updates",
                                {
                                    "type": "send_whatsapp_event",
                                    "data": {
                                        "event": "status_update",
                                        "wa_id": wa_id,
                                        "status": status,
                                        "message_id": msg_id,
                                        "timestamp": raw_timestamp
                                    }
                                }
                            )

            return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            print(" Error al procesar mensaje:", str(e))
            return JsonResponse({'error': 'Formato no valido'}, status=400)


            


@csrf_exempt
def test_enviar_template(request):
    """Vista para enviar un mensaje con plantilla que tiene imagen en el encabezado"""

    wa_id = "573005309990"
    template_name = "plantilla_demo"

    components = [
        {
            "type": "header",
            "parameters": [
                {
                    "type": "image",
                    "image": {
                        "link": "https://r-charts.com/es/miscelanea/procesamiento-imagenes-magick_files/figure-html/importar-imagen-r.png"
                    }
                }
            ]
        },
        {
            "type": "body",
            "parameters": [
                {"type": "text", "text": "César"},
                {"type": "text", "text": "Quiñones"}
            ]
        }
    ]

    resultado = enviar_mensaje_template(wa_id, template_name, "es", components)
    return JsonResponse(resultado)





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
