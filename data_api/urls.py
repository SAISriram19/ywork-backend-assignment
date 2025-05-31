from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('oauth-token/', views.OAuthTokenView.as_view(), name='oauth-token'),
]