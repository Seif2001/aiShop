from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from users.models import User
from .serializers import ConversationSerializer
from drf_spectacular.utils import extend_schema
import json
from .services import Agent
from .functions import function_descriptions, function_inputs, function_schemas, function_registry
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@extend_schema(
    summary="List or create conversations",
    description="GET lists all messages. POST adds a new message.",
    request=ConversationSerializer,
    responses=ConversationSerializer,
    tags=["Conversations"]
)
@api_view(['GET'])
def conversation_list(request):
    if request.method == 'GET':
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)



@extend_schema(
    summary="Retrieve, update, or delete a conversation message",
    description="GET returns one message. PUT updates it. DELETE removes it.",
    request=ConversationSerializer,
    responses=ConversationSerializer,
    tags=["Conversations"]
)
@api_view(['GET', 'PUT', 'DELETE'])
def conversation_detail(request, pk):
    try:
        convo = Conversation.objects.get(pk=pk)
    except Conversation.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ConversationSerializer(convo).data)
    elif request.method == 'PUT':
        serializer = ConversationSerializer(convo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        convo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
@extend_schema(
    summary="Chat with the AI agent",
    description="Chat with the AI agent by sending a user ID and message. The agent will respond based on the provided user ID.",
    request=ConversationSerializer,
    responses=ConversationSerializer,
    tags=["Conversations"]
)



@api_view(['POST'])
@permission_classes([IsAuthenticated])

def chat(request):
    
    print(f"[CHAT] Received request: {request.data}", flush=True)
    user_id = str(request.user.id)  # get from authenticated user
    print("[CHAT] recieved user with id: ", user_id, flush=True)
    message = request.data.get("message")

    if not user_id or not message:
        return Response({"error": "user_id and message are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Save user message
    Conversation.objects.create(user_id=user_id, message=message, direction="user")

    # Handle chat logic
    agent = Agent(user_id, message, function_descriptions=function_descriptions,function_schemas=function_schemas, function_inputs=function_inputs, function_registry=function_registry)
    response = agent.run()

    

    # Save AI response
    Conversation.objects.create(user_id=user_id, message=response, direction="llm")

    return Response({"message": response}, status=status.HTTP_200_OK)



@extend_schema(
    summary="Get all conversations for a specific user",
    description="Retrieve all conversation messages associated with a given user ID.",
    request =ConversationSerializer,
    responses={200: ConversationSerializer(many=True)},
    tags=["Conversations"]
)
@api_view(['GET'])
def get_conversation_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    conversations = Conversation.objects.filter(user=user)
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

