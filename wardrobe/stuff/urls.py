from django.urls import path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemCreateReservationView,
    ItemDetailReservationView,
    ItemUpdateReservationView,
    ItemDeleteReservationView,
    ReservationListView,
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
    path('item/<int:id>/reservation_detail/<int:pk>', ItemDetailReservationView.as_view(), name='item-reservation-detail'),
    path('item/<int:id>/reservation_update/<int:pk>', ItemUpdateReservationView.as_view(), name='item-reservation-update'),
    path('item/<int:id>/reservation_delete/<int:pk>', ItemDeleteReservationView.as_view(), name='item-reservation-delete'),
    path('item/reservations/', ReservationListView.as_view(), name='item-reservation-list'),
    path('about/', views.about, name='stuff-about'),

]
