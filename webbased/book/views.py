from django.shortcuts import render,redirect
from .models import Book,Proof
# Create your views here.


def check_in(request):
    if request.method == 'POST':
        book_type = request.POST.get('book_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_method = request.POST.get('payment_method')
        payment_type = request.POST.get('payment_type')

        if not all([book_type, start_date, end_date, payment_method, payment_type]):
            return redirect("check_in")

        new_booking = Book(
            book_type=book_type, start_date=start_date,
            end_date=end_date, payment_method=payment_method,
            payment_type=payment_type
        )
        

        if not Book.objects.filter(id=new_booking.id).exists():
            new_booking.save()
        return redirect("payment_proof")

    return render(request , "book/book.html")


def payment_proof(request):
    books=Book.objects.all()
    proofs=Proof.objects.all()

    if request.method=='POST':
        img=request.FILES.get("img")

        new_proof=Proof(img=img)
        new_proof.save()
        return render(request, "book/event.html",{
            'books':books,
            'proofs':proofs
        })
        

    return render(request,"book/gcash.html")

