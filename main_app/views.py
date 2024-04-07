
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Book, Author, Publisher
from .serializers import UserSerializer, BookSerializer, AuthorSerializer, PublisherSerializer

# Create your views here.
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the book collector api home route!'}
        return Response(content)

class BookList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer
    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(user=user)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'author': serializer.data})
    def perform_update(self, serializer):
        book = self.get_object()
        if book.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this book."})
        serializer.save()
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this book."})
        instance.delete()   
    
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
##
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })