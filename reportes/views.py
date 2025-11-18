from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from venta.models import Venta
from clientes.models import Cliente

@login_required
def dashboard(request):
    # Estadísticas generales
    total_clientes = Cliente.objects.filter(usuario=request.user).count()
    total_ventas = Venta.objects.filter(usuario=request.user).aggregate(total=Sum('monto'))['total'] or 0
    ventas_mes = Venta.objects.filter(
        usuario=request.user,
        fecha__month=timezone.now().month,
        fecha__year=timezone.now().year
    ).aggregate(total=Sum('monto'))['total'] or 0

    # Clientes por estado
    clientes_por_estado = list(Cliente.objects.filter(usuario=request.user).values('estado').annotate(count=Count('estado')))

    # Ventas recientes
    ventas_recientes = Venta.objects.filter(usuario=request.user).select_related('cliente').order_by('-fecha')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ventas_mes': ventas_mes,
        'clientes_por_estado': clientes_por_estado,
        'ventas_recientes': ventas_recientes,
    }
    return render(request, 'reportes/dashboard.html', context)

def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_panel')
    return render(request, 'index.html')

@login_required
def reportes(request):
    # Reporte general de ventas
    total_ventas = Venta.objects.filter(usuario=request.user).aggregate(total=Sum('monto'))['total'] or 0
    num_ventas = Venta.objects.filter(usuario=request.user).count()
    promedio_venta = total_ventas / num_ventas if num_ventas > 0 else 0

    # Ventas por día del mes actual
    from django.db.models.functions import ExtractDay
    ventas_por_dia = Venta.objects.filter(
        usuario=request.user,
        fecha__month=timezone.now().month,
        fecha__year=timezone.now().year
    ).annotate(
        day=ExtractDay('fecha')
    ).values('day').annotate(total=Sum('monto')).order_by('day')

    # Ranking de clientes por monto
    ranking_monto = Venta.objects.filter(usuario=request.user).values('cliente__nombre').annotate(
        total_compras=Sum('monto')
    ).order_by('-total_compras')[:10]

    # Ranking de clientes por frecuencia
    ranking_frecuencia = Venta.objects.filter(usuario=request.user).values('cliente__nombre').annotate(
        num_compras=Count('cliente')
    ).order_by('-num_compras')[:10]

    # Convertir ventas_por_dia a lista para JSON
    ventas_por_dia_list = list(ventas_por_dia.values('day', 'total'))

    context = {
        'total_ventas': total_ventas,
        'num_ventas': num_ventas,
        'promedio_venta': promedio_venta,
        'ventas_por_mes': json.dumps(ventas_por_dia_list, cls=DjangoJSONEncoder),
        'ranking_monto': ranking_monto,
        'ranking_frecuencia': ranking_frecuencia,
    }
    return render(request, 'reportes/reportes.html', context)
