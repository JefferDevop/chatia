from django.db import models
from django.utils import timezone
from accounts.models import Account  # Asegúrate de que esto apunte a tu modelo de usuario si aplica



class WhatsAppClient(models.Model):
    nombre = models.CharField(max_length=100)
    wa_id = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre


class WhatsAppAgent(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'

    def __str__(self):
        return self.nombre




class WhatsAppConversation(models.Model):
    cliente = models.ForeignKey(WhatsAppClient, on_delete=models.CASCADE)
    agentes = models.ManyToManyField(
        WhatsAppAgent,
        through='WhatsAppConversationAgent',
        related_name='conversaciones'
    )
    inicio_conversacion = models.DateTimeField(default=timezone.now)
    fin_conversacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activa', 'Activa'),
            ('finalizada', 'Finalizada'),
        ],
        default='activa'
    )

    class Meta:
        verbose_name = 'Conversacion'
        verbose_name_plural = 'Conversaciones'

    def __str__(self):
        return f"Conversación con {self.cliente.nombre}"



class WhatsAppConversationAgent(models.Model):
    conversacion = models.ForeignKey(WhatsAppConversation, on_delete=models.CASCADE)
    agente = models.ForeignKey(WhatsAppAgent, on_delete=models.CASCADE)
    asignado_en = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Conversacion_agente'
        verbose_name_plural = 'Conversaciones_agentes'

    def __str__(self):
        return f"{self.agente.nombre} en conversación con {self.conversacion.cliente.nombre}"


class WhatsAppMessage(models.Model):
    conversacion = models.ForeignKey(WhatsAppConversation, on_delete=models.CASCADE, related_name='mensajes')
    tipo = models.CharField(
        max_length=10,
        choices=[
            ('entrante', 'Entrante'),
            ('saliente', 'Saliente'),
        ]
    )
    mensaje = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    visto = models.BooleanField(default=False)
    tiempo_respuesta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"[{self.tipo.upper()}] {self.mensaje[:30]}..."
