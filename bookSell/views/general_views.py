from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres
from django.template.defaulttags import csrf_token
from django.contrib import messages
from django.db.models import F

# page sorting on bookPage
headers = {'cost':'asc',
         'condition':'asc',
         'userSelling':'asc',
         'userRating':'asc'}

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # delete from wishlist
    if(request.GET.get('delfav')):
        print "here"
        wishlist = get_object_or_404(Wishlist, user=request.user, book=book)
        print wishlist
        wishlist.delete()

    sort = request.GET.get('sort') if request.GET.get('sort') is not None else 'cost'
    books_for_sale = BookForSale.objects.filter(book=book_id).order_by(sort)

    ratings = BookRating.objects.filter(book=book_id)
    has_not_reviewed = not any(b.user.user.id == request.user.id for b in ratings)

    # prepare text as needed to wishlist
    inWishlist = len(Wishlist.objects.filter(user=request.user, book=book)) > 0
    wishlistText = "Add to wishlist" if not inWishlist else "Remove from wishlist"
    wishlistName = "add_fav" if not inWishlist else "del_fav"

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
        'has_not_reviewed' : has_not_reviewed,
        'inWishlist' : inWishlist,
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
        return render(request,'books/purchase_history/purchase.html', {'books':books_bought})

def wishlist(request):
    if request.method == "POST":
        book = get_object_or_404(Book, pk=request.POST['book_id'])
        wishlist = Wishlist.objects.filter(user=request.user, book=book).first()
        wishlist.delete()
    
    wishlist = Wishlist.objects.filter(user=request.user)
    books_for_sale = []
    for i,w in enumerate(wishlist):
        book = w.book
        book_for_sale = BookForSale.objects.filter(book=book, cost__lte=w.costLessThan, condition__gte=w.betterConditionThan)
        books_for_sale = books_for_sale  + list(book_for_sale)
    return render(request, 'books/wishlist/wishlist.html', {'wishlist':wishlist, 'books_for_sale' :books_for_sale} )

def selling(request):
    books_sold = BookForSale.objects.filter(userSelling=request.user, sold=True)
    books_for_sale = BookForSale.objects.filter(userSelling=request.user, sold=False)
    profit = sum(b.cost for b in books_sold)
    ratings = UserRating.objects.filter(book__userSelling=1)
    rating = sum(r.rating for r in ratings) / len(ratings) if len(ratings) > 0 else 0

    total_earnings = sum(b.cost for b in books_for_sale) + profit

    return render(request,'books/selling/selling.html', {
        'books_sold':books_sold,
        'books_for_sale': books_for_sale,
        'profit' : profit,
        'total_earnings' : total_earnings,
        'rating' : rating   
        })

def add_fav(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    fav_form = AddFavorite(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        favorite = request.POST.copy()
        favorite['user'] = request.user.id
        favorite['book'] = book.id
        form = AddFavorite(favorite)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wishlist submission successful')
            return HttpResponseRedirect('/book/%s/' % book_id)                                     
        else:
            messages.error(request, 'Wishlist submission unsuccessful')

    # Render the template depending on the context.
    return render(request, 'books/wishlist/add_new.html',{'form': fav_form, 'book': book})

def book_rating(request, book_id):
    book = Book.objects.filter(id=book_id)[0]
    if request.method == 'POST':
        rating = request.POST.copy()
        rating['user'] = UserProfile.objects.filter(user=request.user.id).first().id
        rating['book'] = book.id
        form = BookRatingForm(rating)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submission successful')
            return HttpResponseRedirect('/book/%s/' % book_id)                                     

        # to fix
        else:
            messages.error(request, 'Review submission unsuccessful')
            return render(request, 'books/book_rating.html',{'book_rating': BookRatingForm(), 'book' : book})                                                                        
    else:
        rating_form = BookRatingForm()

    # Render the template depending on the context.
    return render(request, 'books/book_rating.html',{'book_rating': rating_form, 'book': book})



def user_rating(request, book_for_sale):
    book_for_sale = BookForSale.objects.get(id=book_for_sale)
    if request.method == 'POST':
        rating = request.POST.copy()
        rating['book'] = book_for_sale.id
        form = UserRatingForm(rating)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submission successful')
            return HttpResponseRedirect("/purchase_history")                                     

        # to fix
        else:
            messages.error(request, 'Review submission unsuccessful')
            return render(request, 'books/user_rating.html',{'book_rating': rating_form, 'book' : book_for_sale})                                                                        
    else:
        rating_form = BookRatingForm()

    # Render the template depending on the context.
    return render(request, 'books/user_rating.html',{'book_rating': rating_form, 'book': book_for_sale})