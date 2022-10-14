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
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='stuff-home'),
    path('user/<str:username>', UserReservationsListView.as_view(), name='user-reservations'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name='item-delete'),
    path('category', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/new', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('item/<int:pk>/reservation_create', ItemCreateReservationView.as_view(), name='item-reservation-create'),
    path('item/<int:id>/reservation_detail/<int:pk>', ItemDetailReservationView.as_view(), name='item-reservation-detail'),
    path('item/<int:id>/reservation_update/<int:pk>', ItemUpdateReservationView.as_view(), name='item-reservation-update'),
    path('item/<int:id>/reservation_delete/<int:pk>', ItemDeleteReservationView.as_view(), name='item-reservation-delete'),
    path('item/reservations/', ReservationListView.as_view(), name='item-reservation-list'),
    path('about/', views.about, name='stuff-about'),

]
