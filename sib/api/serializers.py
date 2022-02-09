from dataclasses import fields
from rest_framework import serializers

from api.models import Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        # fields = ('id', 'name', 'color', 'slug')
        fields = '__all__'
