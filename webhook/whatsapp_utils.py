import requests
from .models import WhatsAppMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from django.conf import settings

def enviar_mensaje_template(wa_id, template_name, language_code="es", components=None):
    access_token = settings.WHATSAPP_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    url = f'https://graph.facebook.com/v19.0/{phone_number_id}/messages'

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

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    print("➡️ Respuesta de WhatsApp API:", response_data)

    if response.status_code == 200:
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            sender_name="TÚ",
            body=f"[PLANTILLA] {template_name}",
            timestamp=str(int(time.time())),
            direction="OUT"
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "whatsapp_updates",
            {
                "type": "send_whatsapp_event",
                "data": {
                    "event": "new_message",
                    "wa_id": wa_id,
                    "sender_name": "TÚ",
                    "body": f"[PLANTILLA] {template_name}",
                    "timestamp": str(int(time.time())),
                }
            }
        )

    return response_data
