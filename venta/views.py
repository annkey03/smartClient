from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VentaForm
from .models import Venta
from clientes.models import Cliente

@login_required
def venta_list(request):
    ventas = Venta.objects.filter(usuario=request.user).select_related('cliente')
    return render(request, 'venta/venta_list.html', {'ventas': ventas})

@login_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST, user=request.user)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm(user=request.user)
    return render(request, 'venta/venta_form.html', {'form': form})

@login_required
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venta actualizada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm(instance=venta, user=request.user)
    return render(request, 'venta/venta_form.html', {'form': form, 'venta': venta})

@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente.')
        return redirect('venta_list')
    return render(request, 'venta/venta_confirm_delete.html', {'venta': venta})
