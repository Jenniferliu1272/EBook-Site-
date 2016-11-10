from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres, conditions

def condition_view(request):
    canView = True
    return render(request, 'books/individual_book/book_view.html', )

def sell_view(request):
    return render(request, 'books/sellBuyForm/searchExisting.html')

def sell_search(request):
    try:
        query = request.GET['q']
        results = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return render(request, 'books/sellBuyForm/sell_result.html', {'query':query, 'books':results, 'genres' : results[0].get_genre, 'conditions': conditions})
    except:
        return render(request, 'books/sellBuyForm/sell_result.html')

def sell_existing(request, book_id, back):
    if request.method == 'POST':
        current_form = sell_form_existing(request.POST)
        if current_form.is_valid():
            current_form.save_sellFormExisiting(book_id=book_id)
            curr_book = Book.objects.get(id=book_id)
            current_form = sell_form_existing(request.POST, instance=curr_book)
            return render(request, 'books/sellBuyForm/sell_confirm.html', {'sell_form': current_form, 'book': curr_book})
        else:
            return render(request, 'books/sellBuyForm/sell_form.html', {'sell_form': sell_form_existing()})
    else:
        curr_book = Book.objects.get(id=book_id)
        return render(request, 'books/sellBuyForm/sell_form.html', {'sell_form': sell_form_existing(),
                                                                        'book': curr_book})

def sell_original(request):
    if request.method == 'POST':
        current_og_form = sell_form_original(request.POST)
        current_form = sell_form_existing(request.POST)
        if current_form.is_valid():
            new_book = current_og_form.save_sellFormOriginal()
            current_form = current_form.save_sellFormExisiting(book_id=new_book.id)
            book_obj = Book.objects.get(id=new_book.id)
            #current_form = sell_form_existing(request.POST, instance=book_obj)
            return render(request, 'books/sellBuyForm/sell_confirm.html', {'book': book_obj, 'sell_form': current_form })
        else:
            return render(request, 'books/sellBuyForm/sell_original.html', {'sell_form': sell_form_existing(),
                                                                        'sell_form_add': sell_form_original()})
    else:
        return render(request, 'books/sellBuyForm/sell_original.html', {'sell_form': sell_form_existing(),
                                                                    'sell_form_add': sell_form_original()})

def sell_confirm(request, book_id):
    book = Book.objects.get(id=book_id)
    book_sale = BookForSale.objects.get(id=book_id)
    return render(request, 'books/sellBuyForm/sell_confirm.html', {'book': book, 'book_sale': book_sale})


"""def sell_book_view_p1(request, book_id):
    sellform = sell_book_form_p1()
    status = False
    if request.method == 'POST':
        sellForm = sell_book_form_p1(request.POST)
        if sellForm.is_valid():
            new_book = sellForm.save_sell_form_p1()
            status = True
            selfForm2 = sell_book_form_p2()
            return render(request, "books/sell_buy_form/sellForm.html", {'status': status, 'genres' : genres, 'new_book': new_book, 'selfForm2': selfForm2 })
        else:
            status = False
            return render(request, "books/sell_buy_form/sellForm.html", {'status': status, 'genres' : genres})
    else:
        return render(request, "books/sell_buy_form/sellForm.html", {'sellform': sellform, 'genres' : genres, 'status': status})

def sell_book_view_p2(request, book_id):
    status2 = False
    if request.method == 'POST':
        sellForm2 = sell_book_form_p2(request.POST, instance=Book.objects.get(id=book_id))
        if sellForm2.is_valid():
            current_book = sellForm2.save_sell_form_p2(book_id=book_id)
            status2 = True
            return render(request, "books/sell_buy_form/confirm.html", {'status': status2, 'genres' : genres, 'current_book': current_book})
        else:
            status2 = False
            return render(request, "books/sell_buy_form/sellForm.html", {'status': status2, 'genres' : genres})
    else:
        return render(request, "books/sell_buy_form/sellForm.html", {'sellform2': sell_book_form_p2, 'genres' : genres, 'status': status2})"""