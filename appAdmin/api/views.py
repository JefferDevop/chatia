from rest_framework import viewsets
from ..models import Client, Agent, Message, Conversation, Task, Tag, WebhookEvent
from .serializers import (
    ClientSerializer, AgentSerializer, MessageSerializer, 
    ConversationSerializer, TaskSerializer, TagSerializer, WebhookEventSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class WebhookEventViewSet(viewsets.ModelViewSet):
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
