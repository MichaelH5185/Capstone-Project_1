from django.urls import path, include
from . import user_views

app_name = "user"

urlpatterns = [
    path('login/', user_views.loginPage, name="login"),
    path('register/', user_views.registerPage, name="register"),
    path('logout/', user_views.logoutUser, name="logout"),
    path('profile/<int:uid>', user_views.viewProfile, name="view_profile"),
    path('profile/create', user_views.createProfile, name="create_profile"),
    path('profile/update', user_views.updateProfile, name="update_profile"),
    path('reviews/create/<int:uid>', user_views.leaveReview, name="leave_review"),
]