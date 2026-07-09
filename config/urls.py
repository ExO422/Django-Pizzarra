from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect

# Vista manual para asegurar el cierre
def vista_logout(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Ahora usamos la función que definimos arriba
    path('logout/', vista_logout, name='logout'),
    path('', include('tareas.urls')),
]