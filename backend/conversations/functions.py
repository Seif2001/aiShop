
# from pydantic import BaseModel
from langchain.tools import Tool
from orders.models import Order
from orders.serializers import OrderSerializer
from .functions_schemas import GetOrdersInput, UpdateProfileInput, GetOrderInput, GetProductsInput, MakeOrderInput
from users.serializers import UserSerializer
from users.models import User
from products.models import Product
from products.serializers import ProductSerializer

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
    

def get_products()-> dict:
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data
    except Product.DoesNotExist:
        return {"error": "Products not found."}
    

def make_order(user_id: str, product_id: str, quantity:str)->dict:
    order_data = {
        "user": user_id,
        "product": product_id,
        "quantity": quantity
    }
    quantity = int(quantity)

    serializer = OrderSerializer(data=order_data)

    if serializer.is_valid():
        serializer.save()
        return {"success": "Order created successfully.", "order": serializer.data}
    else:
        return {"error": serializer.errors}
    


function_descriptions = {
    "get_orders": {
        "description": "Get all orders for a specific user by providing user_id.",
    },
    "update_profile": {
        "description": "Update a user's profile with the provided data.",
    },
    "get_order": {
        "description": "Get details of a specific order by providing order_id.",
    },
    "get_products":{
        "description": "Get all products found."
    },
    "make_order":{
        "description": "User makes an order to a specific product with a specific quantity"
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
    },
    "get_products":None,
    "make_order":{
        "user_id": "a string representing the user ID, example: '12345'",
        "product_id":"a string representing the product ID, example: '12345'",
        "quantitiy":"a string representing the amount of items the user wants from a specific product"
    }

}

function_schemas = {
    "get_orders": GetOrdersInput,
    "update_profile": UpdateProfileInput,
    "get_order": GetOrderInput,
    "get_products":GetProductsInput,
    "make_order":MakeOrderInput
}

function_registry = {
    "get_orders": get_orders,
    "update_profile": update_profile,
    "get_order": get_order,
    "get_products":get_products,
    "make_order":make_order
}






