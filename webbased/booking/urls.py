from django.urls import path
from . import views

urlpatterns=[
    path("", views.check_in, name="check_in"),
    path("check", views.check_user, name="check_user"),
    path("payment", views.payment_proof, name="proof"),
    path("approved_table", views.payment_approve, name="approve_table")

]