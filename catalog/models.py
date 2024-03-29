from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    """ Model for book genre"""
    name = models.CharField(max_length=200,help_text='Enter a book genre')
    
    def __str__(self):
        return self.name
    
from django.urls import reverse
# used to generate URLs by reversing the URL patterns

class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # Foreign key used because book have only one author but authors can have multiple books
    author = models.ForeignKey('Author', on_delete=models.SET_NULL,null=True)
    
    summary = models.TextField(max_length=1000,help_text='Enter a breif description of the book')
    
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    #Many to many relationship because one book can have many genre and one genre belongs to multiple books
    
    genre = models.ManyToManyField(Genre, help_text = 'Select a genre for this book' )
    
    def display_genre(self):
        # creating string for the genre . this is required to display it since django doesn't allow to display many to many field `genre`
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    
    def __str__(self):
        return self.title
    
    # -----> By default action for form submission <-----
    def get_absolute_url(self):
        #  returns the url to access detail record for this book
        return reverse('book-detail',args=[str(self.id)])
    
    

import uuid # required for unique book instances

class BookInstance(models.Model):
    # Model represeting the specific copy of a book that can be borrowed from the library
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,help_text='Unique id for this particular book across the whole library')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null=True,blank=True)   
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank= True)
    
    MAINTAINANCE = 'm'
    ON_LOAN = 'o'
    RESERVED = 'r'
    AVAILABLE = 'a'
    LOAN_STATUS = (
        (MAINTAINANCE,'Maintenance'),
        (ON_LOAN,'On loan'),
        (RESERVED,'reserved'),
        (AVAILABLE,'available')
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank = True,
        default='m',
        help_text='book availablility'
    )
    
    class Meta:
        ordering = ['due_back']
        # permissions = (("can_mark_returned","Set book as returned"),)

    def __str__(self):
        # string for representing the model object
        return f'{self.id}({self.book.title})'
    
    # -----> By default action for form submission <-----
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.book.id)])

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
    def fine(self):
        finee = 0
        if (date.today() > self.due_back) :
            finee = 1*(date.today()-self.due_back).days
        return finee
            
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField( 'died' ,null = True,blank=True)
    
    class Meta:
        ordering = ['first_name']
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def get_id(self):
        return str(self.id)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    
    
    
    