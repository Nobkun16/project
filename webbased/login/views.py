from django.shortcuts import render,redirect
from .models import Number
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'login/index.html')


def users_dashboard(request):
    users=User.objects.all()
    return render(request, "login/users_dashboard.html",{
        'users':users,
    })


def events_shecdule(request):
    return render(request, "login/events_shecdule.html")


def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"you are now login")
            return render(request, 'login/index.html',{
            "username":username
        })
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect(login_view)


def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("gmail")
        number=request.POST.get("number")
        password=request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"username Already Exist")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exist")
        else:
            user= User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            number=Number(user=user,number=number)
            number.save()

            messages.success(request,"You are now Registered")

            return redirect(index)
    return render(request, 'login/register.html')