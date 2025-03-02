from django.urls import path
from . import views

urlpatterns=[
    path("", views.check_in, name="check_in"),
    path("payment", views.payment_proof, name="payment_proof")
]