from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,Proof
from django.db.models import Q
import hashlib
from django.contrib import messages


# Create your views here.

#redirection to event table
def payment_redirect(request):
    books=Book.objects.all()
    proofs=Proof.objects.all()
    return render(request, "book/event.html",{'books':books,
        'proofs':proofs
        })

#create a hash of img
def file_hash(file):
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(schedule)
        else:
            return redirect(user_dashboard)


def user_dashboard(request):
    user_books=Proof.objects.filter(book__user=request.user)
    return render(request, "login/user_dashboard.html",{
                  "user_books":user_books})
    

def schedule(request):
    schedule='schedule'
    books=Book.objects.all()
    proofs=Proof.objects.all()
    return render(request, "login/admin_panel.html",
           {'books':books,
        'proofs':proofs,
        'schedule':schedule
        })

def payment(request):
    payment='payment'
    books=Book.objects.all()
    proofs=Proof.objects.all()
    return render(request, "login/admin_panel.html",
           {'books':books,
        'proofs':proofs,
        'payment':payment
        })

def event_status(request):
    event_status='event_status'
  
    books=Book.objects.all()
    proofs=Proof.objects.all()
    return render(request, "login/admin_panel.html",
           {'books':books,
        'proofs':proofs,
        'event_status':event_status
        })
    
    

   


#store check in data of customer
def check_in(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            book_type = request.POST.get('book_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            payment_method = request.POST.get('payment_method')
            payment_type = request.POST.get('payment_type')

            overlapped_date=Book.objects.filter(
            Q(start_date__lte=end_date)&Q(end_date__gte=start_date))
        
            if overlapped_date.exists():
                return render(request, "book/book.html", {
                "error":"The Date overlapse"
            })

            new_booking = Book(
            user=request.user,
            book_type=book_type, start_date=start_date,
            end_date=end_date, payment_method=payment_method,
            payment_type=payment_type
        )
            new_booking.save()
            return redirect("payment_proof")
        return render(request, "book/book.html")
    else:
        return redirect("login")

#payment proof is store in database
def payment_proof(request):
    book = Book.objects.last()
    if request.method=='POST':
        img=request.FILES.get("img")
        book=Book.objects.last()
        img_hash=file_hash(img)
        new_proof=Proof(book=book,img=img, hash=img_hash)
        if not Proof.objects.filter(hash=img_hash).exists():
            new_proof.save()
        
        return redirect("index")
    return render(request,"book/gcash.html",{
           'amount':book.amount

    }
              )


#payment status change

def accept_payment(request, proof_id):
    proof=get_object_or_404(Proof, id=proof_id)
    proof.payment_status="Approved"
    proof.save()
    return redirect('approving')


def cancel_payment(request, proof_id):
    proof=get_object_or_404(Proof, id=proof_id)
    proof.payment_status="Declined"
    proof.save()
    return redirect('approving')


def delete_book(request, id):
    book=get_object_or_404(Proof, id=id)
    book.delete()
    return redirect('user_dashboard')


#book status

def cancel_book(request,id):
    book=get_object_or_404(Book, id=id)
    book.refund_status="Pending"
    book.save()
    return redirect('user_dashboard')
    
#refund change status

def refund_complete(request, id):
    if not request.user.is_superuser:
        return redirect('index') 
    
    proof = get_object_or_404(Proof, id=id)
    booking = proof.book

    # Update the refund status
    booking.refund_status = "complete"
    booking.save()
    
    
    messages.success(request, "Refund marked as complete")
    return redirect('refund')

def policies(request):
    return render(request, "book/policies.html")