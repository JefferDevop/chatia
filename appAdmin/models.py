from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import Account
from django.utils import timezone



class Client(models.Model):
    nombre = models.CharField(max_length=100)
    wa_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Agent(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Conversation(models.Model):
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)
    agentes = models.ManyToManyField(Agent, through='ConversationAgent', related_name='conversaciones')
    inicio_conversacion = models.DateTimeField(default=timezone.now)
    fin_conversacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
    ], default='activa')

    def __str__(self):
        return f"Conversación con {self.cliente}"


class ConversationAgent(models.Model):
    conversacion = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    asignado_en = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.agent} en {self.conversacion}" 


class MensajeWhatsApp(models.Model):
    conversacion = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='mensajes')
    tipo = models.CharField(max_length=10, choices=[
        ('entrante', 'Entrante'),
        ('saliente', 'Saliente'),
    ])
    mensaje = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    visto = models.BooleanField(default=False)
    tiempo_respuesta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.tipo.upper()}] {self.mensaje[:30]}..."



# Marca los tipos de clientes preferenciales, por ejemplo, VIP, Regular, etc.
# class Tag(models.Model): 
#     name = models.CharField(max_length=50)
#     color = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name

# class Client(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(blank=True, null=True)
#     tags = models.ForeignKey(Tag, related_name='Tipo Cliente', on_delete=models.CASCADE)  # Default tag is 'Regular'
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Agent(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     available = models.BooleanField(default=True)
#     # skills = models.CharField(max_length=255, blank=True, null=True)  # Skills can be a comma-separated list
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# # class MessageAttachment(models.Model):
# #     message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
# #     file = models.FileField(upload_to='attachments/')
# #     uploaded_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"Attachment for message {self.message.id} - {self.file.name}"
    

# class Conversation(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='Cliente')
#     agent = models.ManyToManyField(Agent, through='ConversationAgent', related_name='Agente')
#     started_at = models.DateTimeField(auto_now_add=True, related_name='Inicio')
#     ended_at = models.DateTimeField(null=True, blank=True, related_name='Fin')
#     status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])

#     def __str__(self):
#         return f"Conversation with {self.client.phone_number} ({self.status})"
#          # return f"Conversation with {self.client.name} ({self.status})"

# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='Conversacion')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     # Generic relation
#     sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     sender_object_id = models.PositiveIntegerField()
#     sender = GenericForeignKey('sender_content_type', 'sender_object_id')

#     def __str__(self):
#         return f"[{self.timestamp}] {self.sender}: {self.content[:30]}"
    


# class ConversationAgent(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
#     agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ('conversation', 'agent')

#     def __str__(self):
#         return f"{self.agent.name} in {self.conversation}"






# class Task(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     description = models.TextField()
#     scheduled_for = models.DateTimeField()
#     completed = models.BooleanField(default=False)
#     assigned_to = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"Task for {self.client.name}"

# class WebhookEvent(models.Model):
#     payload = models.JSONField()
#     received_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Webhook received at {self.received_at}"
