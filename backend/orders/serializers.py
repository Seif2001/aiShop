from rest_framework import serializers
from .models import Order
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Order Example",
            value={
                "user": 1,
                "product": 1,
                "quantity": 2,
                "status": "pending"
            },
            summary="An example of a user order",
            description="Shows a pending order with quantity and foreign key links"
        )
    ]
)
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
