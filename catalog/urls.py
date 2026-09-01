from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('authors/search/', views.author_search, name='author_search'),
    path('genres/search/', views.genre_search, name='genre_search'),
]
