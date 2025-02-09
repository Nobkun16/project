from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Registration(models.Model):
    username=models.CharField(max_length=25, unique=True)
    first_name=models.CharField(max_length=25)
    last_name=models.CharField(max_length=25)
    gmail=models.EmailField(max_length=30,default='example@gmail.com')
    number=models.CharField(max_length=20)
    password=models.CharField(max_length=100)





class Login(models.Model):
    username=models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="login" )
    password=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.username}"
    



class Number(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    number=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.Number}"
    