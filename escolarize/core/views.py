# core/views.py
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # ou qualquer outra URL que você queira redirecionar
        else:
            # Adicionar mensagem de erro ou similar
            pass
    return render(request, 'usuarios/login.html')  # Garante que o template correto seja renderizado

@login_required
def home(request):
    context = {
        'title': 'Dashboard',
        'user': request.user
    }
    return render(request, 'home.html', context)