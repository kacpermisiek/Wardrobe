from django.urls import path
from .views import (
    SetCreateView, SetDetailView, SetDeleteView, SetUpdateView,
    SetTemplateCreateView, SetTemplateDetailView, SetTemplateDeleteView, SetTemplateUpdateView,
    ItemDetailView, ItemDeleteView,
    ReservationConfirmView, ReservationListView, ReservationDetailView, UserReservationListView,
    ReservationUpdateView,
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    ItemTemplateCreateView, ItemTemplateListView, ItemTemplateDetailView, ItemTemplateUpdateView,
    ItemTemplateDeleteView, ReservationDeleteView, ItemTemplateFilterByCategoryView,
    ReservationFilterByUserListView
)
from . import views

category = [
    path('category', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/new', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete')
]

item_template = [
    path('item_template', ItemTemplateListView.as_view(), name='item-template-list'),
    path('item_template/filtered/<int:pk>', ItemTemplateFilterByCategoryView.as_view(), name='item-template-filter'),
    path('item_template/new', ItemTemplateCreateView.as_view(), name='item-template-create'),
    path('item_template/<int:pk>', ItemTemplateDetailView.as_view(), name='item-template-detail'),
    path('item_template/<int:pk>/update', ItemTemplateUpdateView.as_view(), name='item-template-update'),
    path('item_template/<int:pk>/delete', ItemTemplateDeleteView.as_view(), name='item-template-delete'),
]

set_template = [
    path('set_template/create', SetTemplateCreateView.as_view(), name='set-template-create'),
    path('set_template/add_item/<int:template_id>', views.add_item_template_to_set_template,
         name='set-template-add-item'),
    path('set_template/decrement/<int:template_id>', views.decrement_required_item_quantity,
         name='set-template-decrement-item'),
    path('set_template/remove/<int:template_id>', views.remove_item_template_from_set_template,
         name='set-template-remove-item'),
    path('set_template/<int:pk>', SetTemplateDetailView.as_view(), name='set-template-detail'),
    path('set_template/set_current/<int:pk>', views.set_current_set_template, name='set-template-set-current'),
    path('set_template/delete/<int:pk>', SetTemplateDeleteView.as_view(), name='set-template-delete'),
    path('set_template/update/<int:pk>', SetTemplateUpdateView.as_view(), name='set-template-update'),
]

item = [
    path('item/new/<int:template_id>', views.item_create, name='item-create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/delete/<int:pk>', ItemDeleteView.as_view(), name='item-delete'),
]

set = [
    path('set/new/<int:set_template_id>', SetCreateView.as_view(), name='set-create'),
    path('set/detail/<int:pk>', SetDetailView.as_view(), name='set-detail'),
    path('set/delete/<int:pk>', SetDeleteView.as_view(), name='set-delete'),
    path('set/update/<int:pk>', SetUpdateView.as_view(), name='set-update'),
    path('set/request/<int:pk>?<str:start_date>?<str:end_date>', views.set_request, name='set-request'),
]

reservation = [
    path('reservation/new/<int:set_id>?<str:start_date>?<str:end_date>', ReservationConfirmView.as_view(),
         name='reservation-confirm'),
    path('reservation', ReservationListView.as_view(), name='reservation-list'),
    path('user/<int:pk>', ReservationFilterByUserListView.as_view(), name='user-profile'),
    path('user_reservation', UserReservationListView.as_view(), name='reservation-user-list'),
    path('reservation/<int:pk>', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/delete/<int:pk>', ReservationDeleteView.as_view(), name='reservation-delete'),
    path('reservation/update/<int:pk>', ReservationUpdateView.as_view(), name='reservation-update'),
]

urlpatterns = [
    path('', views.home, name='stuff-home'),
    path('about/', views.about, name='stuff-about'),
] + category + item_template + set_template + item + set + reservation
