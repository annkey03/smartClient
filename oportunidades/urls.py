from django.urls import path
from . import views

urlpatterns = [
    path('', views.oportunidad_list, name='oportunidad_list'),
    path('create/', views.oportunidad_create, name='oportunidad_create'),
    path('<int:pk>/edit/', views.oportunidad_update, name='oportunidad_update'),
    path('<int:pk>/delete/', views.oportunidad_delete, name='oportunidad_delete'),
]
