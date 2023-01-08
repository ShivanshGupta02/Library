from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
# Create your views here
import datetime


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required,permission_required
from catalog.forms import RenewBookForm 

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    
    num_authors = Author.objects.count()
    
    # No. of visits to this view using session varaible
    
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1 
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic 

class BookListView(generic.ListView):
    model = Book 
    
class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin

# Creating view for listing all borrowed books for staff members

class BorrowedBooksByUserListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_by_all_user.html'
    paginate_by = 10

    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')
    
    


@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)
    
    # if 'POST' request is made then process the form data 
    if request.method=='POST':
        # create a form instance and populate it with the data from the request(binding)
        form = RenewBookForm(request.POST)
        # if form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as per your requirement
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            print("form is valid")
        #  redirect to a new url
        return HttpResponseRedirect(reverse('all-borrowed'))
        
        
        
    # else 'GET' request is made then prepare the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {
        'form':form,
        'book_instance':book_instance,
    }
    return render(request,'catalog/book_renew_librarian.html',context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author 

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2100'}
    permission_required = 'catalog.can_mark_returned'
    
class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author 
    fields='__all__'
    permission_required= 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author 
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

class AuthorPanelListView(PermissionRequiredMixin,generic.ListView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/author_panel.html'
    paginate_by = 10
  
# creating view for creating, updating and deleting the books

from catalog.models import Book

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book 
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book 
    fields='__all__'
    permission_required = 'catalog.can_mark_returned'
    
    
class BookDelete(PermissionRequiredMixin ,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'
    

class BookPanelListView(PermissionRequiredMixin,generic.ListView):
    model = Book 
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/book_panel.html'
    paginate_by = 10


class AuthorSearchView(LoginRequiredMixin,generic.ListView):
    model = Author
    template_name = 'catalog/author_search.html'
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query=self.request.GET['query']
        context["author_list"] =Author.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        context["query"] = query
        return context

