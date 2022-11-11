from django.urls import path
from .views import (
    SetListView,
    SetTemplateListView, SetTemplateCreateView, SetTemplateDetailView,
    ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView,
    ItemCreateReservationView, ItemDetailReservationView, ItemUpdateReservationView, ItemDeleteReservationView,
    ReservationListView, UserReservationsListView,
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    ItemTemplateCreateView, ItemTemplateListView, ItemTemplateDetailView, ItemTemplateUpdateView,
)
from . import views

urlpatterns = [
    path('', views.home, name='stuff-home'),
    path('set_template/create', SetTemplateCreateView.as_view(), name='set-template-create'),
    path('set_template/add_item/<int:template_id>', views.add_item_template_to_set_template, name='set-template-add-item'),
    path('set_template/<int:pk>', SetTemplateDetailView.as_view(), name='set-template-detail'),
    path('set_template/set_current/<int:pk>', views.set_current_set_template, name='set-template-set-current'),
    path('item_template', ItemTemplateListView.as_view(), name='item-template-list'),
    path('item_template/new', ItemTemplateCreateView.as_view(), name='item-template-create'),
    path('item_template/<int:pk>', ItemTemplateDetailView.as_view(), name='item-template-detail'),
    path('item_template/<int:pk>/update', ItemTemplateUpdateView.as_view(), name='item-template-update'),
    path('item/new/<int:template_id>', views.item_create, name='item-create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    path('item/delete/<int:pk>', ItemDeleteView.as_view(), name='item-delete'),
    path('category', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/new', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    # path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item-update'),
    # path('user/<str:username>', UserReservationsListView.as_view(), name='user-reservations'),
    # path('item/<int:pk>/reservation_create', ItemCreateReservationView.as_view(), name='item-reservation-create'),
    # path('item/<int:pk>/reservation_detail/<int:id>', ItemDetailReservationView.as_view(), name='item-reservation-detail'),
    # path('item/<int:pk>/reservation_update/<int:id>', ItemUpdateReservationView.as_view(), name='item-reservation-update'),
    # path('item/<int:pk>/reservation_delete/<int:id>', ItemDeleteReservationView.as_view(), name='item-reservation-delete'),
    # path('item/reservations/', ReservationListView.as_view(), name='item-reservation-list'),
    path('about/', views.about, name='stuff-about'),

]
