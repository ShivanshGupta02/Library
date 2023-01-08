from django.contrib import admin

# Register your models here.

from .models import Book,BookInstance,Author,Genre

admin.site.register(Genre)
# admin.site.register(Author)
# admin.site.register(BookInstance)
# admin.site.register(Book)

class BookInline(admin.TabularInline):
    model = Book
    

# defining the admin class to change the display on admin web page

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BookInline]

admin.site.register(Author,AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# registering the admin class for book using decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BookInstanceInline]
    

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower','due_back','id')
    list_filter = ('status','due_back')
    fieldsets = (
        ('About the book', {
            "fields": ('book','imprint','id')
        }),
        ('Availablility', {
            "fields": ('status','due_back','borrower')
        }),
    )
    

    
    
    

