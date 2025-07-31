from celery import shared_task
from django.utils import timezone
from .models import WhatsAppConversation
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

from .whatsapp_utils import enviar_mensaje_template
import logging


logger = logging.getLogger(__name__)


@shared_task
def verificar_conversaciones_inactivas():
    """Tarea periódica: finaliza conversaciones que llevan más de 30 minutos inactivas."""
    ahora = timezone.now()
    conversaciones = WhatsAppConversation.objects.filter(estado='activa')
    channel_layer = get_channel_layer()

    for conv in conversaciones:
        ultimo_mensaje = conv.mensajes.order_by('-timestamp').first()

        if not ultimo_mensaje:
            continue  # No hay mensajes, aún no cerrar

        inactiva = ultimo_mensaje.timestamp < ahora - timezone.timedelta(minutes=30)
        if inactiva:
            conv.estado = 'finalizada'
            conv.fin_conversacion = ahora
            conv.save()

            # Emitir evento por WebSocket al frontend
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

    # Limpieza: si ya no hay conversaciones activas, elimina la tarea periódica
    if not WhatsAppConversation.objects.filter(estado='activa').exists():
        PeriodicTask.objects.filter(name='verificar_conversaciones_inactivas').delete()


def iniciar_verificacion_conversaciones():
    """
    Lógica para crear (o recrear) la tarea periódica que monitorea conversaciones activas.
    Esta función debe llamarse desde el webhook o desde otro punto del sistema.
    """
    task_name = 'verificar_conversaciones_inactivas'

    # Si ya existe la tarea, no duplicar
    if PeriodicTask.objects.filter(name=task_name).exists():
        return

    # Si no hay conversaciones activas, no iniciar la tarea
    if not WhatsAppConversation.objects.filter(estado='activa').exists():
        PeriodicTask.objects.filter(name=task_name).delete()
        return

    # Crear intervalo (cada 5 minutos, ajustable)
    intervalo, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.MINUTES,
    )

    # Crear la tarea periódica vinculada a Celery Beat
    PeriodicTask.objects.create(
        interval=intervalo,
        name=task_name,
        task='webhook.tasks.verificar_conversaciones_inactivas',
        args=json.dumps([]),
    )





@shared_task
def enviar_mensaje_template(wa_id, template_name, parametros=None):
    """
    Envía una plantilla de WhatsApp a un cliente de forma asincrónica.
    
    :param wa_id: ID de WhatsApp del cliente (sin +)
    :param template_name: nombre del template registrado en Meta
    :param parametros: diccionario con variables de reemplazo (puede ser None)
    """
    try:
        if parametros is None:
            parametros = {}

        # Llama la función que envía a través de la API de Meta
        enviar_mensaje_template(wa_id, template_name, parametros)
        logger.info(f"✅ Plantilla '{template_name}' enviada a {wa_id} con {parametros}")
    except Exception as e:
        logger.error(f"❌ Error al enviar plantilla a {wa_id}: {str(e)}")


@shared_task
def guardar_log_evento(evento: str, descripcion: str):
    """
    Guarda un log informativo o de advertencia.
    
    :param evento: tipo de evento (ej: mensaje_no_asignado)
    :param descripcion: detalle del evento
    """
    logger.info(f"[LOG EVENTO] {evento}: {descripcion}")


@shared_task
def notificar_admin(mensaje: str):
    """
    Simula una notificación para administradores (puede ser extendido para email, Slack, etc).
    
    :param mensaje: contenido de la notificación
    """
    # En futuro, podrías usar send_mail o Slack API
    print(f"[ADMIN ALERT] ⚠️ {mensaje}")
    logger.warning(f"[NOTIFICACIÓN ADMIN] {mensaje}")






# tasks.py

# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from celery import shared_task
# from django.utils import timezone
# from .models import WhatsAppConversation
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# import json



# @shared_task
# def verificar_conversaciones_inactivas():
#     ahora = timezone.now()
#     conversaciones = WhatsAppConversation.objects.filter(estado='activa')
#     channel_layer = get_channel_layer()

#     for conv in conversaciones:
#         ultimo_mensaje = conv.mensajes.order_by('-timestamp').first()

#         if not ultimo_mensaje:
#             continue  # No hay mensajes, no cerrar aún

#         if ultimo_mensaje.timestamp < ahora - timezone.timedelta(minutes=30):
#             conv.estado = 'finalizada'
#             conv.fin_conversacion = ahora
#             conv.save()

#             # Emitir evento de cierre al frontend
#             wa_id = conv.cliente.wa_id
#             async_to_sync(channel_layer.group_send)(
#                 f"chat_{wa_id}",
#                 {
#                     "type": "send_whatsapp_event",
#                     "data": {
#                         "event": "conversation_closed",
#                         "wa_id": wa_id,
#                         "timestamp": ahora.isoformat()
#                     }
#                 }
#             )

#     # Si ya no hay conversaciones activas, eliminar la tarea periódica
#     if not WhatsAppConversation.objects.filter(estado='activa').exists():
#         from django_celery_beat.models import PeriodicTask
#         PeriodicTask.objects.filter(name='verificar_conversaciones_inactivas').delete()




# def iniciar_verificacion_conversaciones():
#     task_name = 'verificar_conversaciones_inactivas'

#     # Si ya existe, no hacer nada
#     if PeriodicTask.objects.filter(name=task_name).exists():
#         return

#     # Verificar si hay conversaciones activas
#     if not WhatsAppConversation.objects.filter(estado='activa').exists():
#         # Eliminar si existe una tarea previa (por limpieza)
#         PeriodicTask.objects.filter(name=task_name).delete()
#         return



#     # Crear intervalo (cada 5 minutos, por ejemplo)
#     intervalo, _ = IntervalSchedule.objects.get_or_create(
#         every=5,
#         period=IntervalSchedule.MINUTES,
#     )

#     # Crear tarea periódica
#     PeriodicTask.objects.create(
#         interval=intervalo,
#         name=task_name,
#         task='webhook.tasks.verificar_conversaciones_inactivas',
#         args=json.dumps([]),
#     )
