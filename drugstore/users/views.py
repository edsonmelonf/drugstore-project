from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def login(resquest):
    context = {
        "nome":"Name Client"
    }
    return render(resquest,'users/login.html', context)


def register(request):
    return render(request,'users/register.html')