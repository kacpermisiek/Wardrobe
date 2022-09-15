from django.urls import path
from .views import ItemListView, ItemDetailView, ItemCreateView, ItemUpdateView
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='stuff-home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item-update'),
    path('about/', views.about, name='stuff-about'),

]
