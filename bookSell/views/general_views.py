from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres

# page sorting on bookPage
headers = {'cost':'asc',
         'condition':'asc',
         'userSelling':'asc',}
def book(request, book_id):
    sort = request.GET.get('sort') if request.GET.get('sort') is not None else 'cost'
    book = get_object_or_404(Book, pk=book_id)
    books_for_sale = BookForSale.objects.filter(book=book_id).order_by(sort)
    if headers[sort] == "des":
        books_for_sale = books_for_sale.reverse()
        headers[sort] = "asc"
    else:
        headers[sort] = "des"
    return render(request, 'books/individual_book/book_view.html', {'book': book, 'books_for_sale': books_for_sale, 'genres' : genres})

def search(request):
    query = request.GET['q']
    results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'books/search/search_results.html', {'query':query, 'books':results, 'genres' : genres})

def genre(request, genre):
    books = Book.objects.filter(genre=genres.index(genre)).order_by('rating')
    top_book = books[0]
    new_book = Book.objects.filter(genre=genres.index(genre)).order_by('year_published')[0]
    return render(request, 'books/browse_genre/genre.html', {'genre': genre, 'genres' : genres, 'books': books, 'top_book':top_book, 'new_book': new_book})

def condition_view(request):
    canView = True
    return render(request, 'books/individual_book/book_view.html', )
