from officer.models import ProductList
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product_id')
    text = serializers.CharField(source='product_name')

    class Meta:
        model = ProductList
        fields = ('id', 'text')
