from django.urls import path
from .views import Home, BookList, BookDetail, AuthorList, AuthorDetail, AuthorBooks

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetail.as_view(), name='book-detail'),
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<int:id>/', AuthorDetail.as_view(), name='author-detail'),
    path('authors/<int:id>/books/', AuthorBooks.as_view(), name='author-books'),
    
]