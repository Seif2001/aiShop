from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="List or create orders",
    description="GET lists all orders. POST places a new order.",
    request=OrderSerializer,
    responses=OrderSerializer,
    tags=["Orders"]
)
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Retrieve, update, or delete an order",
    description="GET returns an order. PUT updates it. DELETE cancels it.",
    request=OrderSerializer,
    responses=OrderSerializer,
    tags=["Orders"]
)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(OrderSerializer(order).data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @extend_schema(
#     summary="Get all orders for a specific user",
#     description="Returns a list of orders placed by the user with the given ID.",
#     responses=OrderSerializer,
#     tags=["Orders"]
# )
# @api_view(['GET'])
# def get_my_orders(request, user_id):
#     orders = Order.objects.filter(user_id=user_id)
#     if not orders.exists():
#         return Response({"message": "No orders found for this user."}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)