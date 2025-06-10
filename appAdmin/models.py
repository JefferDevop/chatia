from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import Account



# Marca los tipos de clientes preferenciales, por ejemplo, VIP, Regular, etc.
class Tag(models.Model): 
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, default='Regular', blank=True)  # Default tag is 'Regular'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Agent(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    # skills = models.CharField(max_length=255, blank=True, null=True)  # Skills can be a comma-separated list
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class MessageAttachment(models.Model):
#     message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
#     file = models.FileField(upload_to='attachments/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Attachment for message {self.message.id} - {self.file.name}"
    

class Conversation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])

    def __str__(self):
        return f"Conversation with {self.client.phone_number} ({self.status})"
         # return f"Conversation with {self.client.name} ({self.status})"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Generic relation
    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')

    def __str__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content[:30]}"
    


class ConversationAgent(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('conversation', 'agent')

    def __str__(self):
        return f"{self.agent.name} in {self.conversation}"






class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField()
    scheduled_for = models.DateTimeField()
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Task for {self.client.name}"

class WebhookEvent(models.Model):
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook received at {self.received_at}"
