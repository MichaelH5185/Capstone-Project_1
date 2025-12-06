from django.urls import path, include
from . import board_views

app_name = "board"

urlpatterns =[
    path('boards/create', board_views.create_board, name="create_board"),
    path('boards/delete/<int:bid>/', board_views.delete_board, name="delete_board"),
    path('boards/edit/<int:bid>/', board_views.edit_board, name="edit_board"),
    path('boards/view/<int:bid>/', board_views.display_board, name="display_board"),
    path('boards', board_views.board_home, name="board_home"),
]