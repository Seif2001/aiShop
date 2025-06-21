from rest_framework import serializers
from .models import Product
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Product Example",
            value={
                "name": "Noise Cancelling Headphones",
                "price": "199.99",
                "quantity": 3
            },
            summary="A product listing example",
            description="Shows a product with its name and price"
        )
    ]
)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
