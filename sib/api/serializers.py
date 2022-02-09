from django.contrib.auth import get_user_model
from rest_framework import serializers

# from .models import Deal

User = get_user_model()


class APIDealSerializer(serializers.ModelSerializer):
    gems = serializers.SerializerMethodField()
    counter = 0
    good_clients = {}

    class Meta:
        model = User
        fields = ('username', 'spent_money', 'gems')

    def get_gems(self, obj):
        if not self.counter:
            self.clients_deals()

        # Thanks python for updating ^_^
        client_items = self.good_clients.pop(self.counter)

        result = set()
        for items in self.good_clients.values():
            result.update(client_items.intersection(items))
        self.good_clients[self.counter] = client_items
        self.counter += 1
        return [item for (item,) in result]

    def clients_deals(self):
        for client in self.instance:
            self.good_clients[self.counter] = set(
                client.deals.select_related('item').values_list('item')
            )
            self.counter += 1
        self.counter = 0

    def save(self, **kwargs):
        self.counter = 0
        super().save(**kwargs)
