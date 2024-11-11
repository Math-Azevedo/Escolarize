# escolarize/urls.py
from django.contrib import admin
from django.urls import path, include
from usuarios.views import home_view, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),  # Página inicial
    path('usuarios/', include('usuarios.urls')),  # Se necessário
    path('notas/', include('notas.urls')),  # Se necessário
    path('mensagens/', include('mensagens.urls')),  # Esta linha é importante!
]
