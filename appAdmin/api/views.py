# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Client, Agent, Conversation, ConversationAgent, MensajeWhatsApp
from .serializers import (
    ClientSerializer, AgentSerializer,
    ConversationSerializer, MensajeWhatsAppSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer



class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def perform_create(self, serializer):
        # Aquí podrías automatizar la asignación de agentes
        serializer.save()


class MensajeWhatsAppViewSet(viewsets.ModelViewSet):
    queryset = MensajeWhatsApp.objects.all()
    serializer_class = MensajeWhatsAppSerializer




class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=["get"])
    def mensajes(self, request, pk=None):
        conversacion = self.get_object()
        mensajes = conversacion.mensajes.all().order_by("timestamp")
        serializer = MensajeWhatsAppSerializer(mensajes, many=True)
        return Response(serializer.data)

