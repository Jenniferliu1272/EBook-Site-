from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres, conditions

def sell_view(request):

    return render(request, 'books/sellBuyForm/searchExisting.html', {'genres': genres, 'genre': genres[0]})

def sell_search(request):
    try:
        query = request.GET['q']
        results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return render(request, 'books/sellBuyForm/sell_result.html', {'query':query, 'books':results, 'genres' : results[0].get_genre, 'conditions': conditions})
    except:
        return render(request, 'books/sellBuyForm/sell_result.html')

def sell_existing(request, book_id, back):
    if request.user.is_authenticated():
        if request.method == 'POST':
            current_form = sell_form_existing(request.POST)
            if current_form.is_valid():
                current_form.save_sellFormExisiting(book_id=book_id,user=request.user)
                curr_book = Book.objects.get(id=book_id)
                current_form = sell_form_existing(request.POST, instance=curr_book)
                return render(request, 'books/sellBuyForm/sell_confirm.html', {'sell_form': current_form, 'book': curr_book})
            else:
                return render(request, 'books/sellBuyForm/sell_form.html', {'sell_form': sell_form_existing()})
        else:
            curr_book = Book.objects.get(id=book_id)
            return render(request, 'books/sellBuyForm/sell_form.html', {'sell_form': sell_form_existing(),
                                                                            'book': curr_book})
    else:
        return redirect('books/homepage/index.html')

def sell_original(request):
    if request.method == 'POST':
        current_og_form = sell_form_original(request.POST)
        current_form = sell_form_existing(request.POST)
        if current_form.is_valid():
            new_book = current_og_form.save_sellFormOriginal()
            current_form = current_form.save_sellFormExisiting(book_id=new_book.id, user=request.user)
            book_obj = Book.objects.get(id=new_book.id)
            return render(request, 'books/sellBuyForm/sell_confirm.html', {'book': book_obj, 'sell_form': current_form })
        else:
            return render(request, 'books/sellBuyForm/sell_original.html', {'sell_form': sell_form_existing(),
                                                                        'sell_form_add': sell_form_original(), })
    else:
        return render(request, 'books/sellBuyForm/sell_original.html', {'sell_form': sell_form_existing(),
                                                                    'sell_form_add': sell_form_original()})

def sell_confirm(request, book_id):
    book = Book.objects.get(id=book_id)
    book_sale = BookForSale.objects.get(id=book_id)
    return render(request, 'books/sellBuyForm/sell_confirm.html', {'book': book, 'book_sale': book_sale})

