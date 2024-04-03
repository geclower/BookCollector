
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

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