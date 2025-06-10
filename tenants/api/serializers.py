from rest_framework.serializers import ModelSerializer
from ..models import Client

# from warehome.api.serializers import StockSerializer

class CustomerSerializer(ModelSerializer):
    # stock_data = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = Client
        fields = ['id_n', 'company' ]

