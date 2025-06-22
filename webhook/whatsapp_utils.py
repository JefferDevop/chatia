import time
from datetime import datetime
import pytz
import requests
from decouple import config
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import WhatsAppMessage, WhatsAppClient, WhatsAppConversation


def enviar_mensaje_template(wa_id, template_name, language_code="es", components=None):
    """
    Envía un mensaje de plantilla de WhatsApp usando la API Graph de Meta.

    Args:
        wa_id (str): Número de WhatsApp del destinatario (con código de país).
        template_name (str): Nombre de la plantilla configurada en Meta Business Manager.
        language_code (str): Código del idioma (por defecto "es").
        components (list): Componentes opcionales del mensaje (header, body, buttons, etc.).

    Returns:
        dict: Respuesta JSON de la API de WhatsApp.
    """

    access_token = config('WHATSAPP_TOKEN')
    phone_number_id = config('WHATSAPP_PHONE_NUMBER_ID')
    url = f'https://graph.facebook.com/v23.0/{phone_number_id}/messages'

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": wa_id,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
        }
    }

    if components:
        payload["template"]["components"] = components

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    print("➡️ Respuesta de WhatsApp API:", response_data)

    if response.status_code == 200:
        raw_timestamp = int(time.time())  # Unix timestamp
        timestamp = datetime.fromtimestamp(raw_timestamp, tz=pytz.UTC) 

        # Registrar mensaje saliente
        cliente, _ = WhatsAppClient.objects.get_or_create(wa_id=wa_id, defaults={"nombre": "nombre del cliente"})
        conversacion, _ = WhatsAppConversation.objects.get_or_create(
            cliente=cliente, estado='activa', defaults={'inicio_conversacion': timestamp}
        )


        WhatsAppMessage.objects.create(
            conversacion=conversacion,
            tipo='saliente',
            mensaje=f"[TEMPLATE: {template_name}]",  # marcador opcional
            timestamp=timestamp,
            message_id=response_data.get('messages', [{}])[0].get('id', ''),
            visto=False
        )


        # Notificación por canal
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "whatsapp_updates",
            {
                "type": "send_whatsapp_event",
                "data": {
                    "event": "new_message",
                    "wa_id": wa_id,
                    "sender_name": "TÚ",
                    "message_body": f"[PLANTILLA] {template_name}",
                    "wa_timestamp": timestamp.isoformat(),
                    "message_type": "sent",
                }
            }
        )

    return response_data
