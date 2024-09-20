from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('how-to-apply', views.how_to_apply, name="how-to-apply"),
    path('contact-us', views.contact_us, name="contact-us"),
    path('about-us', views.about_us, name="about-us"),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"), #logout user
]