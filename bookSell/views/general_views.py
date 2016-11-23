from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres
from django.template.defaulttags import csrf_token
from django.contrib import messages

# page sorting on bookPage
headers = {'cost':'asc',
         'condition':'asc',
         'userSelling':'asc'}
def book(request, book_id):
    sort = request.GET.get('sort') if request.GET.get('sort') is not None else 'cost'
    book = get_object_or_404(Book, pk=book_id)
    books_for_sale = BookForSale.objects.filter(book=book_id).order_by(sort)
    #has_not_reviewed = not any(b['user'] == request.user.id for b in books_for_sale)
    ratings = BookRating.objects.filter(book=book_id)
    if headers[sort] == "des":
        books_for_sale = books_for_sale.reverse()
        headers[sort] = "asc"
    else:
        headers[sort] = "des"
    return render(request, 'books/individual_book/book_view.html', {
        'book': book,
        'books_for_sale': books_for_sale,
        'len': len(books_for_sale),
        'genres' : genres, 
        'ratings':ratings,
        #'has_not_reviewed' : has_not_reviewed
        })

def search(request):
    query = request.GET['q']
    results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'books/search/search_results.html', {'query':query, 'books':results, 'genres' : genres})

def genre(request, genre):
    # TODO fix when rating
    top_books = Book.objects.filter(genre=genres.index(genre)).order_by('year_published')
    if(len(top_books) == 0):
        return render(request,'books/browse_genre/genre_empty.html', {'genre': genre, 'genres' : genres})

    new_books = Book.objects.filter(genre=genres.index(genre)).order_by('year_published')
    return render(request, 'books/browse_genre/genre.html', {'genre': genre, 'genres' : genres, 'books': top_books, 'top_book':top_books[0], 'new_book': new_books[0]})

def condition_view(request):
    canView = True
    return render(request, 'books/individual_book/book_view.html', )
	
def purchase_history(request):
	books_bought = BookForSale.objects.filter(userBought=request.user)
	if(len(books_bought) == 0):
		return render(request,'books/purchase_history/purchase_empty.html')
	else:
		books = Book.objects.filter(title = books_bought[0].book.title)
		for b in books_bought[1:]:
			books = books | Book.objects.filter(title = b.book.title)
		return render(request,'books/purchase_history/purchase.html', {'books':books})


def book_rating(request, book_id):
    book = Book.objects.filter(id=book_id)[0]
    if request.method == 'POST':
        rating_form = BookRatingForm(data=request.POST)
        rating = request.POST.copy()
        rating['user'] = request.user.id
        rating['book'] = book.id
        form = BookRatingForm(rating)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submission successful')
            return HttpResponseRedirect('/book/%s/' % book_id)                                     

        # to fix
        else:
            messages.success(request, 'Review submission unsuccessful')
            return render(request, 'books/book_rating.html',{'book_rating': rating_form, 'book' : book})                                                                        
    else:
        rating_form = BookRatingForm()

    # Render the template depending on the context.
    return render(request, 'books/book_rating.html',{'book_rating': rating_form, 'book': book})