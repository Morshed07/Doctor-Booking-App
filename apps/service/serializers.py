from rest_framework import serializers
from .models import Service
from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'description',
            'products',
            'lab_recommended'
        ]
