from django.contrib import admin
from .models import PostIt

@admin.register(PostIt)
class PostItAdmin(admin.ModelAdmin):
    # Columnas que se verán en el listado del admin
    list_display = ('titulo', 'color', 'completada', 'creado_el')
    
    # Filtros laterales para búsqueda rápida
    list_filter = ('completada', 'color', 'creado_el')
    
    # Campo de búsqueda en la parte superior
    search_fields = ('titulo', 'contenido')
    
    # Edición rápida desde el listado (opcional, muy útil)
    list_editable = ('completada', 'color')