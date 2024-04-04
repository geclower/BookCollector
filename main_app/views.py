
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Book, Author, Publisher
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer

# Create your views here.
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the book collector api home route!'}
        return Response(content)

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'author': serializer.data})
    
class AddAuthorToBook(APIView):
    def post(self, request, book_id, author_id):
        book = Book.objects.get(id=book_id)
        author = Author.objects.get(id=author_id)
        book.authors.add(author)
        return Response({'message': f'Author {author.name} added to Book {book.title}'})
##
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'

class AuthorBooks(generics.ListCreateAPIView):
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id)
    def perform_create(self, serializer):
        author_id = self.kwargs['author_id']
        author = Author.objects.get(id=author_id)
        serializer.save(author=author)
##
class PublisherList(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class PublisherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    lookup_field = 'id'

class PublisherBooks(generics.ListCreateAPIView):
    def get_queryset(self):
        publisher_id = self.kwargs['publisher_id']
        return Book.objects.filter(publisher_id=publisher_id)
    def perform_create(self, serializer):
        publisher_id = self.kwargs['publisher_id']
        publisher = Publisher.objects.get(id=publisher_id)
        serializer.save(publisher=publisher)
