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

    def validate(self, data):
        product = data.get('product')
        quantity_requested = data.get('quantity')

        if not product:
            raise serializers.ValidationError("Product must be provided.")

        if quantity_requested > product.quantity:
            raise serializers.ValidationError(
                f"Requested quantity ({quantity_requested}) exceeds available stock ({product.available_quantity})."
            )
        return data

    def create(self, validated_data):
        product = validated_data['product']
        product.quantity -= validated_data['quantity']
        product.save()

        return super().create(validated_data)
