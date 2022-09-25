from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre
# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic 

class BookListView(generic.ListView):
    model = Book 
    
class BookDetailView(generic.ListView):
    model = Book
    
class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author