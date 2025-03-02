from django.db import models



# Create your models here.

class Book(models.Model):
    book_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_method = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.book_type} from {self.start_date} to {self.end_date}"
    

class Proof(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
    ]
    img = models.ImageField(upload_to='payment_proof/')
    payment_status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="pending")

    def __str__(self):
        return f"{self.payment_status}"

    
