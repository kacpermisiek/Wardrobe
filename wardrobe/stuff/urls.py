from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stuff-home'),
    path('about/', views.about, name='stuff-about'),

]
