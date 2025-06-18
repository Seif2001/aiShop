from rest_framework import serializers
from .models import Conversation
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Conversation Message Example",
            value={
                "user_id": 2,
                "message": "Where is my order?",
                "direction": "user"
            },
            summary="User message to AI",
            description="Stores a user or LLM message with timestamp and direction"
        )
    ]
)
class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
