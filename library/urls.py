from django.urls import path

from . import views
from .views import LoanedBooksByUser

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.book_list, name='books'),
    path('books/<int:pk>', views.book_detail, name='book-detail'),
    path('search/', views.search, name='search'),
    path('mybooks/', LoanedBooksByUser, name='my-borrowed'),
    path('mybooks/<uuid:pk>', views.BookByUserDetailView.as_view(), name='my-book'),
    path('mybooks/new', views.BookByUserCreateView.as_view(), name='my-borrowed-new'),
    path('mybooks/<uuid:pk>/update', views.BookByUserUpdateView.as_view(), name='my-book-update'),
    path('mybooks/<uuid:pk>/delete', views.BookByUserDeleteView.as_view(), name='my-book-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profilis, name='profile'),
]