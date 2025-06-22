from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import datetime
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..whatsapp_utils import enviar_mensaje_template





from rest_framework import viewsets, permissions
from ..models import WhatsAppClient, WhatsAppAgent, WhatsAppConversation, WhatsAppConversationAgent, WhatsAppMessage
from .serializers import (
    WhatsAppClientSerializer,
    WhatsAppAgentSerializer,
    WhatsAppConversationSerializer,
    WhatsAppMessageSerializer,
    WhatsAppConversationAgentSerializer,
)



# ViewSets
class WhatsAppClientViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppClient.objects.all()
    serializer_class = WhatsAppClientSerializer


class WhatsAppAgentViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppAgent.objects.all()
    serializer_class = WhatsAppAgentSerializer


class WhatsAppConversationViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppConversation.objects.all()
    serializer_class = WhatsAppConversationSerializer


class WhatsAppConversationAgentViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppConversationAgent.objects.all()
    serializer_class = WhatsAppConversationAgentSerializer


class WhatsAppMessageViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppMessage.objects.all()
    serializer_class = WhatsAppMessageSerializer





# Webhook View
class WhatsAppWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == 'demo':
            return HttpResponse(challenge)
        return HttpResponse("Forbidden", status=403)

    def post(self, request):
        try:
            data = request.data
            channel_layer = get_channel_layer()

            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})

                    if 'messages' in value:
                        message_data = value['messages'][0]
                        wa_id = message_data['from']
                        texto = message_data['text']['body']
                        # message_id = message_data.get('id', 'unknown_id')
                        raw_timestamp = message_data['timestamp']
                        timestamp = datetime.fromtimestamp(int(raw_timestamp), tz=pytz.UTC)
                        sender_name = value['contacts'][0]['profile']['name']

                        # Cliente
                        cliente, _ = WhatsAppClient.objects.get_or_create(
                            wa_id=wa_id,
                            defaults={"nombre": sender_name}
                        )

                        # Conversación activa o crear una nueva
                        conversacion, creada = WhatsAppConversation.objects.get_or_create(
                            cliente=cliente,
                            estado='activa',
                            defaults={"inicio_conversacion": timestamp}
                        )

                        # Mensaje
                        try:
                            WhatsAppMessage.objects.create(
                                conversacion=conversacion,
                                tipo='entrante',
                                mensaje=texto,
                                timestamp=timestamp
                            )
                        except IntegrityError:
                            continue

                        # Emitir al canal
                        async_to_sync(channel_layer.group_send)(
                            f"chat_{wa_id}",
                            {
                                "type": "send_whatsapp_event",
                                "data": {
                                    "event": "new_message",
                                    "wa_id": wa_id,
                                    "sender_name": sender_name,
                                    "body": texto,
                                    "timestamp": timestamp.isoformat(),
                                },
                            },
                        )

                    elif 'statuses' in value:
                        for status_info in value['statuses']:
                            msg_id = status_info['id']
                            status = status_info['status']
                            raw_timestamp = int(status_info['timestamp'])
                            timestamp = datetime.fromtimestamp(raw_timestamp, tz=pytz.UTC)
                            wa_id = status_info['recipient_id']

                            # Mensaje existente
                            try:
                                mensaje = WhatsAppMessage.objects.get(id=msg_id)
                                mensaje.visto = (status == 'read')
                                mensaje.save()
                            except WhatsAppMessage.DoesNotExist:
                                pass

                            async_to_sync(channel_layer.group_send)(
                                f"chat_{wa_id}",
                                {
                                    "type": "send_whatsapp_event",
                                    "data": {
                                        "event": "status_update",
                                        "wa_id": wa_id,
                                        "status": status,
                                        "message_id": msg_id,
                                        "timestamp": timestamp.isoformat(),
                                    },
                                },
                            )

            return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)






# # views.py
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import AllowAny
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from django.http import HttpResponse
# from django.http import JsonResponse
# from django.db import IntegrityError
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from datetime import datetime
# import pytz
# import json
# from ..models import WhatsAppMessage, WhatsAppContact, WhatsAppMessageStatus

# from ..whatsapp_utils import enviar_mensaje_template


# # @method_decorator(csrf_exempt, name='dispatch')
# class WhatsAppWebhookAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):

#         mode = request.GET.get('hub.mode')
#         token = request.GET.get('hub.verify_token')
#         challenge = request.GET.get('hub.challenge')

#         if mode == 'subscribe' and token == 'demo':
#             return HttpResponse(challenge)
#         return HttpResponse("Forbidden", status=403)

#     def post(self, request):

#         try:
#             data = request.data
#             channel_layer = get_channel_layer()

#             print("🔌 Redis conectado:", channel_layer)

#             for entry in data.get('entry', []):
#                 for change in entry.get('changes', []):
#                     value = change.get('value', {})

#                     # Mensaje entrante
#                     if 'messages' in value:
#                         print("Datos recibidos:", value)
#                         message_data = value['messages'][0]
#                         wa_id = message_data['from']
#                         texto = message_data['text']['body']
#                         message_id = message_data.get('id', 'unknown_id')
#                         raw_timestamp = message_data['timestamp']
#                         timestamp = datetime.fromtimestamp(int(raw_timestamp), tz=pytz.UTC)
#                         sender_name = value['contacts'][0]['profile']['name']

#                         # Guardar mensaje
#                         try:
#                             WhatsAppMessage.objects.create(
#                                 wa_id=wa_id,
#                                 sender_name=sender_name,
#                                 message_body=texto,
#                                 wa_timestamp=timestamp,
#                                 message_type='IN',
#                                 message_id=message_id
#                             )
#                         except IntegrityError:
#                             print(f"⚠️ Mensaje duplicado ignorado: {message_id}")
#                             continue

#                         # Crear o actualizar contacto
#                         contacto, creado = WhatsAppContact.objects.get_or_create(
#                             wa_id=wa_id,
#                             defaults={"nombre": sender_name, "last_interaction": timestamp}
#                         )

#                         if not creado:
#                             contacto.nombre = sender_name  # Actualiza el nombre si cambia
#                             contacto.last_interaction = timestamp
#                             contacto.save()

#                                             # Enviar al frontend
#                         async_to_sync(channel_layer.group_send)(
#                             "whatsapp_updates",
#                             {
#                                 "type": "send_whatsapp_event",
#                                 "data": {
#                                     "event": "new_message",
#                                     "wa_id": wa_id,
#                                     "sender_name": sender_name,
#                                     "body": texto,
#                                     "timestamp": timestamp.isoformat()
#                                 }
#                             }
#                         )

#                     #  Estados (delivered, read)
#                     elif 'statuses' in value:
#                         print("Datos de estado recibidos:", value)
#                         for status_info in value['statuses']:
#                             msg_id = status_info['id']
#                             status = status_info['status']
#                             raw_timestamp = int(status_info['timestamp'])
#                             timestamp = datetime.fromtimestamp(raw_timestamp, tz=pytz.UTC)
#                             wa_id = status_info['recipient_id']

#                             # Datos opcionales
#                             conversation_id = status_info.get('conversation', {}).get('id')
#                             category = status_info.get('pricing', {}).get('category')
#                             pricing_model = status_info.get('pricing', {}).get('pricing_model')

#                             WhatsAppMessageStatus.objects.create(
#                                 message_id=msg_id,
#                                 wa_id=wa_id,
#                                 status=status,
#                                 timestamp=timestamp,
#                                 conversation_id=conversation_id,
#                                 category=category,
#                                 pricing_model=pricing_model
#                             )

#                             # Actualizar contacto si existe
#                             try:
#                                 contacto = WhatsAppContact.objects.get(wa_id=wa_id)
#                                 contacto.last_interaction = timestamp
#                                 contacto.save()
#                             except WhatsAppContact.DoesNotExist:
#                                 pass

#                             # Enviar al frontend
#                             async_to_sync(channel_layer.group_send)(
#                                 "whatsapp_updates",
#                                 {
#                                     "type": "send_whatsapp_event",
#                                     "data": {
#                                         "event": "status_update",
#                                         "wa_id": wa_id,
#                                         "status": status,
#                                         "message_id": msg_id,
#                                         "timestamp": timestamp.isoformat()
#                                     }
#                                 }
#                             )

#             return JsonResponse({'status': 'ok'}, status=200)

#         except Exception as e:
#             print(" Error al procesar mensaje:", str(e))
#             return JsonResponse({'error': 'Formato no valido'}, status=400)


            


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











