from django.urls import path
from . import views

login_url_name="url"

urlpatterns=[
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("verification", views.generate_otp, name="otp"),


    path("amenities", views.amenities, name="amenities"),
    path("contact", views.contact, name="contact"),
    path("about_us", views.about_us, name="about_us"),

    path("event_data", views.event_data, name="event_data" )

]