from django.shortcuts import render,redirect,get_object_or_404
from .models import Number
from book.models import Book
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


# Create your views here.



#redirect
def amenities(request):
    return render(request, 'login/amenities.html')

def contact(request):
    return render(request, 'login/contact.html')

def about_us(request):
    return render(request, 'login/about.html')


def index(request):
    return render(request, 'login/homepage.html')

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)

        if user is not None:
            request.session['username']=username
        
            return redirect(generate_otp)
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
            return redirect(login_view)

        return redirect(login_view)
    return render(request, 'login/register.html')

def generate_otp(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user = get_object_or_404(User, username=username)

    
    if 'otp_secret_key' not in request.session:
        request.session['otp_secret_key'] = pyotp.random_base32()

    otp_secret_key = request.session['otp_secret_key']
    totp = pyotp.TOTP(otp_secret_key)
    otp_code = totp.now()

    if request.method == 'POST':
        user_otp = request.POST.get('otp')

        # Verify if the user OTP is valid
        if totp.verify(user_otp, valid_window=1):  
            login(request, user)
            request.session.modified = True
            del request.session['otp_secret_key']
            del request.session['username']
            return redirect('index')  
        else:
            return render(request, 'login/otp.html', {
                'otp': otp_code
            })

    send_mail(
        'OTP Code',
        f'Your OTP code is: {otp_code} ',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )

    return render(request, 'login/otp.html', {'otp': otp_code,})


def event_data(request):
    data=[]
    books=Book.objects.all()
    
    for book in books:
        data.append({
            "title":'Booked',
            "start":book.start_date.isoformat()
        })

    return JsonResponse(data, safe=False)