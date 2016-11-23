from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres, conditions


def buy_book(request, book_id):
    if request.method == 'POST' and request.user.is_authenticated():
        buying_form = buy_form(request.POST)
        if buying_form.is_valid():
            buying_form.save()
            book_for_sale = BookForSale.objects.get(id=book_id)
            book = Book.objects.get(id=book_id)
            book_for_sale.userBought = request.user
            book_for_sale.save()
            return render(request, 'books/buy_form/buy.html', {'buy_form': buying_form, 'book': book })
        else:
            return render(request, 'books/buy_form/buy.html', {'buy_form': buy_form()})
    else:
        return render(request, 'books/buy_form/buy.html', {'buy_form': buy_form()})
