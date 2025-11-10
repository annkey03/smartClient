from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OportunidadForm
from .models import Oportunidad
from clientes.models import Cliente

@login_required
def oportunidad_list(request):
    oportunidades = Oportunidad.objects.filter(usuario=request.user).select_related('cliente')
    return render(request, 'oportunidades/oportunidad_list.html', {'oportunidades': oportunidades})

@login_required
def oportunidad_create(request):
    if request.method == 'POST':
        form = OportunidadForm(request.POST, user=request.user)
        if form.is_valid():
            oportunidad = form.save(commit=False)
            oportunidad.usuario = request.user
            oportunidad.save()
            messages.success(request, 'Oportunidad creada exitosamente.')
            return redirect('oportunidad_list')
    else:
        form = OportunidadForm(user=request.user)
    return render(request, 'oportunidades/oportunidad_form.html', {'form': form})

@login_required
def oportunidad_update(request, pk):
    oportunidad = get_object_or_404(Oportunidad, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = OportunidadForm(request.POST, instance=oportunidad, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oportunidad actualizada exitosamente.')
            return redirect('oportunidad_list')
    else:
        form = OportunidadForm(instance=oportunidad, user=request.user)
    return render(request, 'oportunidades/oportunidad_form.html', {'form': form, 'oportunidad': oportunidad})

@login_required
def oportunidad_delete(request, pk):
    oportunidad = get_object_or_404(Oportunidad, pk=pk, usuario=request.user)
    if request.method == 'POST':
        oportunidad.delete()
        messages.success(request, 'Oportunidad eliminada exitosamente.')
        return redirect('oportunidad_list')
    return render(request, 'oportunidades/oportunidad_confirm_delete.html', {'oportunidad': oportunidad})
