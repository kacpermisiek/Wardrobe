from django.urls import path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemCreateReservationView,
    UserReservationsListView,
)
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='stuff-home'),
    path('user/<str:username>', UserReservationsListView.as_view(), name='user-reservations'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/reservation_create', ItemCreateReservationView.as_view(), name='item-reservation-create'),
    path('about/', views.about, name='stuff-about'),

]
