





# from pydantic import BaseModel
from langchain.tools import Tool
from orders.models import Order
from orders.serializers import OrderSerializer
from .functions_schemas import GetOrdersInput, UpdateProfileInput, GetOrderInput
from users.models import User
from users.serializers import UserSerializer


def get_orders(user_id:str) -> str:
    orders = Order.objects.filter(user_id=user_id)
    if not orders.exists():
        return "You have no orders."
    return "\n".join(
        f"Order #{o.id}: {o.product.name} x{o.quantity} ({o.status})" for o in orders
    )


def update_profile(user_id: str, data: dict) -> dict:
    print(f"[AI TOOL] Called update_profile with user_id={user_id}, data={data}")

    try:
        user = User.objects.get(id=user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return UserSerializer(user).data
    except User.DoesNotExist:
        return {"error": "User not found."}


def get_order(order_id: str) -> dict:
    try:
        order = Order.objects.get(id=order_id)
        return OrderSerializer(order).data
    except Order.DoesNotExist:
        return {"error": "Order not found."}
    


function_descriptions = {
    "get_orders": {
        "description": "Get all orders for a specific user by providing user_id.",
    },
    "update_profile": {
        "description": "Update a user's profile with the provided data.",
    },
    "get_order": {
        "description": "Get details of a specific order by providing order_id.",
    }
}


function_inputs = {
    "get_orders": {
        "user_id": "a string representing the user ID, example: '12345'"
    },
    "update_profile": {
        "user_id": "a string representing the user ID, example: '12345'",
        "data": "a dictionary with profile fields to update"
    },
    "get_order": {
        "order_id": "a string representing the order ID, example: '67890'"
    }
}

function_schemas = {
    "get_orders": GetOrdersInput,
    "update_profile": UpdateProfileInput,
    "get_order": GetOrderInput
}






