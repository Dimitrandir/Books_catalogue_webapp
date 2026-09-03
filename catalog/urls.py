from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('authors/search/', views.author_search, name='author_search'),
    path('genres/search/', views.genre_search, name='genre_search'),
    path('authors/quick-create/', views.author_quick_create, name='author_quick_create'),
    path('genres/quick-create/', views.genre_quick_create, name='genre_quick_create'),
    path('publishers/quick-create/', views.publisher_quick_create, name='publisher_quick_create'),
]
