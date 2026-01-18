from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.detail import DetailView

from .models import Library
from .models import Book

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
def list_books(request):
  books = Book.objects.all()
  return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
  mode =Library
  template_name = 'relationship_app/library_detail.html'
  context_object_name = 'library'

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # logs user in immediately
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

  