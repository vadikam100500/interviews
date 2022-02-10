from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class APIDealSerializer(serializers.ModelSerializer):
    gems = serializers.SerializerMethodField()
    counter = 0
    good_clients = {}

    class Meta:
        model = User
        fields = ('username', 'spent_money', 'gems')

    def get_gems(self, obj):
        """
        Create dict with items of all users if it is first call.
        Return list with common items, that was bought by that user and others.
        """
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
        """
        Insert values like {<number of user>: <set items of that user> }
        into good_clients:dict
        """
        for client in self.instance:
            self.good_clients[self.counter] = set(
                client.deals.select_related('item').values_list('item')
            )
            self.counter += 1
        self.counter = 0

        # smx = set(
        #     User.objects.row('SELECT good_customers.username, api_deal.item '
        #                      'FROM '
        #                      '(SELECT users_user.id, users_user.username '
        #                      'FROM 'users_user ORDER BY spent_money DESC '
        #                      'LIMIT 5) as good_customers '
        #                      'JOIN api_deal '
        #                      'ON good_customers.id=api_deal.customer_id '
        #                      'GROUP BY '
        #                      'good_customers.username, api_deal.item')
        # )
        # >>> AttributeError: 'UserManager' object has no attribute 'row'
        # --> sadly(
        # I would not expand UserManager,
        # because i have difficult interview tommorow, sorry

        # (self.instance.
        #  select_related('deals__item')
        #  .values_list('username', 'deals__item'))
        # >>> first 5 items of 1 user, because instance query have LIMIT 5
        # --> sadly(
