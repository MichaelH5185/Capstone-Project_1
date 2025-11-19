from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create_listing, name='create_listing'),
    path('message/<int:listing_id>/', views.send_message, name='send_message'),
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
    path('accounts/register/', views.register, name='register'),
]
