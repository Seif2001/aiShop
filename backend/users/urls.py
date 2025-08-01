from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.user_list),             # GET all users or POST new user
    path('<int:pk>/', views.user_detail),  # GET/PUT/DELETE a single user
    path('login/', views.login),
    path('signup/', views.signup),


]
