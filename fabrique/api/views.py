from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from notifications.models import Mailing, Message
from api import serializers

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.CustomUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tag', 'operator_сode')


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = serializers.MailingSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MailinglistSerializer
        return serializers. MailingSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
