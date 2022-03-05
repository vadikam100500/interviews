from django.contrib.auth import get_user_model
from rest_framework import serializers

from notifications.models import Mailing, Message

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'phone',
                  'operator_сode', 'tag', 'time_zone')
        model = User

    def validate(self, data):
        phone = self.data.get('phone')
        if phone[0] != '7' or len(phone) != 11:
            raise serializers.ValidationError(
                'Введите номер в формате 7XXXXXXXXXX'
            )
        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'send_time', 'status', 'mailing', 'contact'
        )
        model = Message


class MailinglistSerializer(serializers.ModelSerializer):
    send_messages = serializers.SerializerMethodField()
    not_send_messages = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'start_date', 'end_date',
            'text', 'tag_filter', 'code_filter', 'send_messages',
            'not_send_messages'
        )
        model = Mailing

    def get_send_messages(self, obj):
        return obj.messages.filter(status='S').count()

    def get_not_send_messages(self, obj):
        return obj.messages.filter(status='N').count()


class MailingSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'start_date', 'end_date',
            'text', 'tag_filter', 'code_filter', 'messages'
        )
        model = Mailing

    def validate(self, data):
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        if start_date > end_date:
            raise serializers.ValidationError(
                'Начало рассылки должно быть раньше окончания'
            )
        return data
