from django.urls import path, include
from . import board_views

app_name = "board"

urlpatterns =[
    path('create', board_views.create_board, name="create_board"),
    path('delete/<int:bid>/', board_views.delete_board, name="delete_board"),
    path('edit/<int:bid>/', board_views.edit_board, name="edit_board"),
    path('view/<int:bid>/', board_views.display_board, name="display_board"),
    path("view/<int:bid>/reply/", board_views.post_board_message, name="post_board_message"),
    path("view/messages/<int:bmid>/delete/", board_views.delete_board_message, name="delete_board_message"),
    path('', board_views.board_home, name="board_home"),
]