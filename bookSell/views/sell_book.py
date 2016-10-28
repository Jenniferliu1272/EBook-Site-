from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres

def condition_view(request):
    canView = True
    return render(request, 'books/individual_book/book_view.html', )

def sell_book_view_p1(request, book_id):
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
        return render(request, "books/sell_buy_form/sellForm.html", {'sellform2': sell_book_form_p2, 'genres' : genres, 'status': status2})