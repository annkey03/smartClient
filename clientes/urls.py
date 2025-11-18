from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('create/', views.cliente_create, name='cliente_create'),
    path('<int:pk>/edit/', views.cliente_update, name='cliente_update'),
    path('<int:pk>/delete/', views.cliente_delete, name='cliente_delete'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Admin URLs
    path('admin/', views.admin_panel, name='admin_panel'),
    path('admin/user/create/', views.user_create, name='user_create'),
    path('admin/user/<int:pk>/edit/', views.user_update, name='user_update'),
    path('admin/user/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('admin/company-type/create/', views.company_type_create, name='company_type_create'),
    path('admin/company-type/<int:pk>/edit/', views.company_type_update, name='company_type_update'),
    path('admin/company-type/<int:pk>/delete/', views.company_type_delete, name='company_type_delete'),
]
