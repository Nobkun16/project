from django.shortcuts import render, redirect
from .models import Book, Proof
from django.contrib import messages

def check_in(request):
    if request.method == 'POST':
        book_type = request.POST.get('book_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_method = request.POST.get('payment_method')
        payment_type = request.POST.get('payment_type')

        if not all([book_type, start_date, end_date, payment_method, payment_type]):
            messages.error(request, "All fields are required!")
            return redirect("check_in")

        new_booking = Book(
            book_type=book_type, start_date=start_date,
            end_date=end_date, payment_method=payment_method,
            payment_type=payment_type
        )
        new_booking.save()

        if payment_method == 'gcash':
            return render(request, "booking/gcash.html")

    return render(request, "booking/book.html")

def check_user(request):
    if request.user.is_authenticated:
        return redirect('check_in')

    messages.warning(request, 'Login first')
    return redirect('login')

def payment_proof(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        new_book=Book.objects.last()
        
        new_proof = Proof( book=new_book,img=img)
        new_proof.save()
        return render(request, 'booking/payment_approve.html')

def payment_approve(request):
    proofs = Proof.objects.all()
    return render(request, 'booking/payment_approve.html', {
        'proofs': proofs
    })
