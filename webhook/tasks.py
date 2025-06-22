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
    expiradas = WhatsAppConversation.objects.filter(
        estado='activa',
        inicio_conversacion__lt=ahora - timezone.timedelta(minutes=30)
    )

    if not expiradas.exists():
        from django_celery_beat.models import PeriodicTask
        PeriodicTask.objects.filter(name='verificar_conversaciones_inactivas').delete()
        return

    channel_layer = get_channel_layer()
    for conv in expiradas:
        conv.estado = 'finalizada'
        conv.fin_conversacion = ahora
        conv.save()

        # Emitir evento de cierre
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
