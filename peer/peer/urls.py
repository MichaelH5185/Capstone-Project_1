from django.urls import path, include
from . import views

app_name = "peer"

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', include('peer.user.user_urls', namespace="user")),
    #path('board/', include('peer.board.board_urls')),
    path('listing/', include('peer.listing.listing_urls')), 
    path('create/', views.create_listing, name='create_listing'),
    path('message/<int:listing_id>/', views.send_message, name='send_message'),
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
    path('skills/create', views.create_new_skill, name="create-skill")
    #path('accounts/register/', views.register, name='register'),
]
