from rest_framework.viewsets import ModelViewSet

from api.models import Deal
from api.serializers import DealSerializer


class DealViewSet(ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
