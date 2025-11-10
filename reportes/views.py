from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
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
    clientes_por_estado = Cliente.objects.filter(usuario=request.user).values('estado').annotate(count=Count('estado'))

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
    return render(request, 'index.html')

@login_required
def reportes(request):
    # Reporte general de ventas
    total_ventas = Venta.objects.filter(usuario=request.user).aggregate(total=Sum('monto'))['total'] or 0
    num_ventas = Venta.objects.filter(usuario=request.user).count()
    promedio_venta = total_ventas / num_ventas if num_ventas > 0 else 0

    # Ventas por mes (últimos 12 meses)
    ventas_por_mes = Venta.objects.filter(
        usuario=request.user,
        fecha__gte=timezone.now() - timezone.timedelta(days=365)
    ).extra(select={'month': "EXTRACT(month FROM fecha)", 'year': "EXTRACT(year FROM fecha)"}).values('year', 'month').annotate(total=Sum('monto')).order_by('year', 'month')

    # Ranking de clientes por monto
    ranking_monto = Venta.objects.filter(usuario=request.user).values('cliente__nombre').annotate(
        total_compras=Sum('monto')
    ).order_by('-total_compras')[:10]

    # Ranking de clientes por frecuencia
    ranking_frecuencia = Venta.objects.filter(usuario=request.user).values('cliente__nombre').annotate(
        num_compras=Count('cliente')
    ).order_by('-num_compras')[:10]

    context = {
        'total_ventas': total_ventas,
        'num_ventas': num_ventas,
        'promedio_venta': promedio_venta,
        'ventas_por_mes': ventas_por_mes,
        'ranking_monto': ranking_monto,
        'ranking_frecuencia': ranking_frecuencia,
    }
    return render(request, 'reportes/reportes.html', context)
