from django.contrib.auth import get_user_model
from rest_framework import serializers

# from .models import Deal

User = get_user_model()


class APIDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'spent_money')
