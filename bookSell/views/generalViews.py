from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import ourUser, Book, BookForSale
from django.db.models import Q

# page sorting on bookPage
headers = {'cost':'asc',
         'condition':'asc',
         'userSelling':'asc',}

def bookPage(request, book_id):
    sort = request.GET.get('sort') if request.GET.get('sort') is not None else 'cost'
    book = get_object_or_404(Book, pk=book_id)
    books_for_sale = BookForSale.objects.filter(book=book_id).order_by(sort)
    if headers[sort] == "des":
        books_for_sale = books_for_sale.reverse()
        headers[sort] = "asc"
    else:
        headers[sort] = "des"
    return render(request, 'books/book_view.html', {'book': book, 'books_for_sale': books_for_sale})

def userPage(request, user_id):
    return HttpResponse("You're looking at user %s." % user_id)

def search(request):
    query = request.GET['q']
    results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'books/search_results.html', {'query':query, 'books':results})

def condition_view(request):
    canView = True
    return render(request, 'books/book_view.html', )

