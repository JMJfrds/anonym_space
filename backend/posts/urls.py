from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/reply/', views.add_reply, name='add_reply'), # MUHIM
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]