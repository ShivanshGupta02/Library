from django.shortcuts import render,redirect
from .models import Book,BookInstance,Author,Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .mixins import CheckStaffGroupMixin 
from django.views import View
from django.contrib.auth.models import User
# Create your views here
import datetime


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse 
from django.contrib.auth.decorators import login_required,permission_required
# from catalog.forms import RenewBookForm 

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_instances_available = BookInstance.objects.filter(status=BookInstance.AVAILABLE).count()
    
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

class BorrowedBooksByUserListView(CheckStaffGroupMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_by_all_user.html'
    paginate_by = 10

    
    def get_queryset(self):
        # return BookInstance.objects.filter(status__exact='o')
        return BookInstance.objects.filter(status=BookInstance.ON_LOAN)
    

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author 

class AuthorCreate(CheckStaffGroupMixin, CreateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2100'}
      
class AuthorUpdate(CheckStaffGroupMixin,UpdateView):
    model = Author 
    fields='__all__'
   
class AuthorDelete(CheckStaffGroupMixin,DeleteView):
    model = Author 
    success_url = reverse_lazy('authors')
    
class AuthorPanelListView(CheckStaffGroupMixin,generic.ListView):
    model = Author
    template_name = 'catalog/author_panel.html'
    paginate_by = 10
  
# creating view for creating, updating and deleting the books

from catalog.models import Book

class BookCreate(CheckStaffGroupMixin , CreateView):
    model = Book 
    fields = '__all__'

class BookUpdate(CheckStaffGroupMixin, UpdateView):
    model = Book 
    fields='__all__'
   
    
class BookDelete(CheckStaffGroupMixin , DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    
class BookInstanceCreate(CheckStaffGroupMixin, CreateView):
    model = BookInstance
    fields = ['book','imprint','status']

class BookPanelListView(CheckStaffGroupMixin, generic.ListView):
    model = Book 
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
    
from catalog.models import BookInstance
class MarkReturned(CheckStaffGroupMixin,View):
        def get(self,request,*args,**kwargs):
            bookInstance_id = self.kwargs["pk"]
            obj = BookInstance.objects.get(id=bookInstance_id)
            obj.due_back = None 
            obj.status = 'a'
            obj.borrower = None 
            obj.save(update_fields=['due_back','status','borrower'])
            return redirect(reverse('all-borrowed'))


from .forms import IssueBookForm
class availableBooks(CheckStaffGroupMixin,View):
        template_name = 'catalog/book_issue.html'
        form_class = IssueBookForm
        def get(self,request,*args,**kwargs):
            context = {}
            form = self.form_class()
            context['form'] = form
            context["available_book_list"] = BookInstance.objects.filter(Q(status=BookInstance.AVAILABLE)) 
            return render(request,self.template_name,context)
        
        def post(self,request,*args,**kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                bookInstance_id = form.cleaned_data['bookInstance_id']
                due_back_date = form.cleaned_data['due_back_date']
                username = form.cleaned_data['username']
                # print(type(bookInstance_id))
                # print(type(username))
                # print(type(due_back_date))  
                # print(bookInstance_id)
                # print(username)
                # print(due_back_date)
                user_object = User.objects.get(username=username)
                           
                
                obj = BookInstance.objects.get(pk=bookInstance_id)
                obj.due_back = due_back_date
                obj.borrower = user_object
                # SETTING STATUS ON LOAN
                obj.status =  BookInstance.ON_LOAN
                obj.save(update_fields=['due_back','borrower','status'])
                return HttpResponse("Book Successfully Issued")
            return render(request,self.template_name,{'form':form})

         
        