from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list),
    path('<int:pk>/', views.order_detail),
    # path('user/<int:user_id>/', views.get_my_orders),  

]
