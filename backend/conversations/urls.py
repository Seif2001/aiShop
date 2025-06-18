from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list),
    path('<int:pk>/', views.conversation_detail),
    path('chat/', views.chat),
    path('user/<int:user_id>/', views.get_conversation_by_user),
]
