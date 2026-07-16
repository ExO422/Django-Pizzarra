from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PostIt

@login_required
def pizarra(request):
    if request.method == 'POST' and request.user.is_superuser:
        v_titulo = request.POST.get('titulo')
        v_contenido = request.POST.get('contenido')
        v_color = request.POST.get('color')
        usuario_id = request.POST.get('usuario_asignado')
        
        # Se asigna la tarea al usuario seleccionado por el admin
        if usuario_id:
            usuario = User.objects.get(id=usuario_id)
            PostIt.objects.create(titulo=v_titulo, contenido=v_contenido, color=v_color, asignado_a=usuario)
        
        return redirect('pizarra')
    
    # Enviamos todos los usuarios para el selector del admin
    usuarios = User.objects.all()
    
    # Filtro: Admin ve todo, usuario normal solo sus propias tareas pendientes
    if request.user.is_superuser:
        postits_pendientes = PostIt.objects.filter(completada=False).order_by('-creado_el')
    else:
        postits_pendientes = PostIt.objects.filter(completada=False, asignado_a=request.user).order_by('-creado_el')
    
    return render(request, 'pizarra.html', {
        'postits': postits_pendientes, 
        'usuarios': usuarios
    })

@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(PostIt, id=tarea_id)
    tarea.completada = True
    tarea.save()
    return redirect('pizarra')

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(PostIt, id=tarea_id)
    if tarea.completada: return redirect('pizarra')
    
    if request.method == 'POST' and request.user.is_superuser:
        tarea.titulo = request.POST.get('titulo')
        tarea.contenido = request.POST.get('contenido')
        tarea.color = request.POST.get('color')
        
        # Capturamos la reasignación
        usuario_id = request.POST.get('usuario_asignado')
        if usuario_id:
            tarea.asignado_a = User.objects.get(id=usuario_id)
            
        tarea.save()
        return redirect('pizarra')
        
    usuarios = User.objects.all() # Necesario para el select en editar.html
    return render(request, 'editar.html', {'tarea': tarea, 'usuarios': usuarios})

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(PostIt, id=tarea_id)
    if not tarea.completada:
        tarea.delete()
    return redirect('pizarra')

@login_required
def historial_completadas(request):
    # Filtro: Admin ve todo, usuario normal solo sus propias tareas completadas
    if request.user.is_superuser:
        postits_completados = PostIt.objects.filter(completada=True).order_by('-creado_el')
    else:
        postits_completados = PostIt.objects.filter(completada=True, asignado_a=request.user).order_by('-creado_el')
    return render(request, 'completadas.html', {'postits': postits_completados})

@login_required
def detalle_completada(request, tarea_id):
    tarea = get_object_or_404(PostIt, id=tarea_id)
    return render(request, 'detalle.html', {'tarea': tarea})