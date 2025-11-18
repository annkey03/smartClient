from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Cliente, CompanyType

# Register your models here.

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'empresa', 'estado', 'usuario')
    list_filter = ('estado', 'empresa', 'usuario')
    search_fields = ('nombre', 'correo', 'empresa__name')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

# Customize User admin to show is_superuser
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_superuser',)
    list_filter = UserAdmin.list_filter + ('is_superuser',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
