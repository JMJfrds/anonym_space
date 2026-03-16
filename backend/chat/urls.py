from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_dashboard, name='chat_list'),
    path('<int:user_id>/', views.chat_dashboard, name='chat_room'),
]