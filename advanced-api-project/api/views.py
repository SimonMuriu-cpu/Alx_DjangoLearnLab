from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Book
from .serializers import BookSerializer

from django_filters import rest_framework
from rest_framework import filters


class BookListView(generics.ListAPIView):

  """
    DetailView for retrieving a single book by ID.
    Provides a read-only endpoint to retrieve a specific Book instance.
    """
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [AllowAny]
  
  # Add filtering capabilities

  filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
  filterset_fields = ['publication_year', 'author']
  
  # Add search capabilities
  search_fields = ['title', 'author_name']

    # Add search and ordering capabilities

  ordering_fields = ['title', 'publication_year']
  ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Provides a read-only endpoint to retrieve a specific Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]



class BookCreateView(generics.CreateAPIView):
  """
    CreateView for adding a new book.
    Provides a write-only endpoint to create a new Book instance.
    """
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]
  
  def perform_create(self, serializer):
      serializer.save()


class BookUpdateView(generics.UpdateAPIView):
  """
    UpdateView for modifying an existing bookD.
    Provides an endpoint to update existing Book instance.
    """
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]
  def perform_update(self, serializer):
      serializer.save()

class BookDeleteView(generics.DestroyAPIView):
  """
    DeleteView for removing a book by ID.
    Provides an endpoint to delete a specific Book instance.
    """
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated]