from django.urls import path, include
from . import user_views

app_name = "user"

urlpatterns = [
    path('login/', user_views.loginPage, name="login"),
    path('register/', user_views.registerPage, name="register"),
    path('logout/', user_views.logoutUser, name="logout"),
]