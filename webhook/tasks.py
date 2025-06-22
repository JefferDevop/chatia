# tasks.py

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from django.utils import timezone
from .models import WhatsAppConversation
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json



@shared_task
def verificar_conversaciones_inactivas():
    ahora = timezone.now()
    conversaciones = WhatsAppConversation.objects.filter(estado='activa')
    channel_layer = get_channel_layer()

    for conv in conversaciones:
        ultimo_mensaje = conv.mensajes.order_by('-timestamp').first()

        if not ultimo_mensaje:
            continue  # No hay mensajes, no cerrar aún

        if ultimo_mensaje.timestamp < ahora - timezone.timedelta(minutes=30):
            conv.estado = 'finalizada'
            conv.fin_conversacion = ahora
            conv.save()

            # Emitir evento de cierre al frontend
            wa_id = conv.cliente.wa_id
            async_to_sync(channel_layer.group_send)(
                f"chat_{wa_id}",
                {
                    "type": "send_whatsapp_event",
                    "data": {
                        "event": "conversation_closed",
                        "wa_id": wa_id,
                        "timestamp": ahora.isoformat()
                    }
                }
            )

    # Si ya no hay conversaciones activas, eliminar la tarea periódica
    if not WhatsAppConversation.objects.filter(estado='activa').exists():
        from django_celery_beat.models import PeriodicTask
        PeriodicTask.objects.filter(name='verificar_conversaciones_inactivas').delete()




def iniciar_verificacion_conversaciones():
    task_name = 'verificar_conversaciones_inactivas'

    # Si ya existe, no hacer nada
    if PeriodicTask.objects.filter(name=task_name).exists():
        return

    # Verificar si hay conversaciones activas
    if not WhatsAppConversation.objects.filter(estado='activa').exists():
        # Eliminar si existe una tarea previa (por limpieza)
        PeriodicTask.objects.filter(name=task_name).delete()
        return



    # Crear intervalo (cada 5 minutos, por ejemplo)
    intervalo, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.MINUTES,
    )

    # Crear tarea periódica
    PeriodicTask.objects.create(
        interval=intervalo,
        name=task_name,
        task='webhook.tasks.verificar_conversaciones_inactivas',
        args=json.dumps([]),
    )
