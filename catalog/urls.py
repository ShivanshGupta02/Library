from django.urls import path
from . import views
import uuid

# Here pk stands for primary key
urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name='books'),   
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('author/create/',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/update/',views.AuthorUpdate.as_view(),name='author-update'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
    path('author/panel/',views.AuthorPanelListView.as_view(),name='author-panel'),
    path('author/search/',views.AuthorSearchView.as_view(),name='author-search'),
]

urlpatterns += [
    path('book/create/',views.BookCreate.as_view(),name='book-create'),
    path('book/<int:pk>/update/',views.BookUpdate.as_view(),name='book-update'),
    path('book/<int:pk>/delete/',views.BookDelete.as_view(),name='book-delete'),
    path('bookInstance/create/',views.BookInstanceCreate.as_view(),name='bookinstance-create'),
    path('book/panel/',views.BookPanelListView.as_view(),name='book-panel'),
    path('book/issue/',views.availableBooks.as_view(),name='book-issue'),
]

urlpatterns+=[
    path('allbooks/',views.BorrowedBooksByUserListView.as_view(),name='all-borrowed')
]
urlpatterns+=[
    path('bookInstance/<uuid:pk>/return/',views.MarkReturned.as_view(),name ='mark-bookinstance-returned')
]

urlpatterns += [
    path('signin/',views.signin,name="signin"),
    path('signup/',views.signup,name="signup"),
    path('signout/',views.signout,name="signout"),
]




