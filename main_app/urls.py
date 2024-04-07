from django.urls import path
from .views import Home, BookList, BookDetail, AuthorList, AuthorDetail, AuthorBooks, PublisherList, PublisherDetail, PublisherBooks, AddAuthorToBook, CreateUserView, LoginView, VerifyUserView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetail.as_view(), name='book-detail'),
    path('books/<int:book_id>/add_author/<int:author_id>/', AddAuthorToBook.as_view(), name='add-author-to-book'),
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<int:id>/', AuthorDetail.as_view(), name='author-detail'),
    path('authors/<int:id>/books/', AuthorBooks.as_view(), name='author-books'),
    path('publishers/', PublisherList.as_view(), name='publisher-list'),
    path('publishers/<int:id>/', PublisherDetail.as_view(), name='Publisher-detail'),
    path('publishers/<int:id>/books/', PublisherBooks.as_view(), name='publisher-books'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh')
]