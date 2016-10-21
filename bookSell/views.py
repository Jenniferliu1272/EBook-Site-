from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from .models import Book, BookForSale

def index(request):
    top_books = Book.objects.order_by('-rating')[:5]
    new_books = Book.objects.order_by('-year_published')[:5]
    return render(request, 'books/homepage/index.html', {'top_books': top_books, 'new_books': new_books})

def bookPage(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    books_for_sale = BookForSale.objects.filter(book=book_id)
    return render(request, 'books/book_view.html', {'book': book, 'books_for_sale': books_for_sale})

def userPage(request, user_id):
    return HttpResponse("You're looking at user %s." % user_id)
