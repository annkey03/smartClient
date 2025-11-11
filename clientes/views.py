from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import RegistroForm, ClienteForm
from .models import Cliente, CompanyType

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'cliente': cliente})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Admin views
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin_panel(request):
    users = User.objects.all()
    company_types = CompanyType.objects.all()
    return render(request, 'clientes/admin_panel.html', {
        'users': users,
        'company_types': company_types,
    })

@user_passes_test(is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('admin_panel')
    else:
        form = RegistroForm()
    return render(request, 'clientes/user_form.html', {'form': form})

@user_passes_test(is_superuser)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # Handle form submission for user update
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('admin_panel')
    return render(request, 'clientes/user_form.html', {'user': user})

@user_passes_test(is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('admin_panel')
    return render(request, 'clientes/user_confirm_delete.html', {'user': user})

@user_passes_test(is_superuser)
def company_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        CompanyType.objects.create(name=name, description=description)
        messages.success(request, 'Tipo de empresa creado exitosamente.')
        return redirect('admin_panel')
    return render(request, 'clientes/company_type_form.html')

@user_passes_test(is_superuser)
def company_type_update(request, pk):
    company_type = get_object_or_404(CompanyType, pk=pk)
    if request.method == 'POST':
        company_type.name = request.POST.get('name')
        company_type.description = request.POST.get('description')
        company_type.save()
        messages.success(request, 'Tipo de empresa actualizado exitosamente.')
        return redirect('admin_panel')
    return render(request, 'clientes/company_type_form.html', {'company_type': company_type})

@user_passes_test(is_superuser)
def company_type_delete(request, pk):
    company_type = get_object_or_404(CompanyType, pk=pk)
    if request.method == 'POST':
        company_type.delete()
        messages.success(request, 'Tipo de empresa eliminado exitosamente.')
        return redirect('admin_panel')
    return render(request, 'clientes/company_type_confirm_delete.html', {'company_type': company_type})
