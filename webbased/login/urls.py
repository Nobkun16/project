from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("usersdashboard", views.users_dashboard, name="users_dashboard"),
    path("events", views.events_shecdule, name="events_shecdule" )

]