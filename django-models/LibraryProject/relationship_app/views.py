from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView

from relationship_app.models import Book, Library

# Create your views here.
def list_books(request):
  books = Book.objects.all()
  return render(request, 'relationship_app/book_list.html', {'books': books})

class LibraryDetailView(DetailView):
  mode =Library
  template_name = 'relationship_app/library_detail.html'
  context_object_name = 'library'

  