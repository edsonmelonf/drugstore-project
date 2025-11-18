from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")  
        else:
            return render(request, "users/login.html", {
                "error": "Usuário ou senha incorretos"
            })

    return render(request, "users/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

    
        if password != confirm:
            return render(request, 'users/register.html', {
                'error': 'As senhas não coincidem'
            })


        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                'error': 'Usuário já existe'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        return redirect('users:login')

    return render(request, 'users/register.html')