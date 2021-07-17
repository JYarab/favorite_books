from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('user/<int:id>', views.user_page),
    path('books', views.books),
    path('books/create', views.create_book),
    path('books/<int:id>', views.book_page),
    path('books/<int:id>/fav', views.favorite_book),
    path('books/<int:id>/edit', views.edit_book),
    path('books/<int:id>/delete', views.delete_book),
    
]