from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres, conditions
from django.contrib import messages


def buy_book(request, book_id):
    book_for_sale = BookForSale.objects.filter(id=book_id)[0]
    book = book_for_sale.book
    if request.POST:
        new_form = buy_form(request.POST)
        if new_form.is_valid():
            new_obj = new_form.save(commit=False)
            new_obj.user = request.user
            new_obj.book = book_for_sale
            new_obj.save()

            book_for_sale.sold = True
            book_for_sale.userBought = request.user
            book_for_sale.save()
            messages.success(request, 'Purchase successful')
            return HttpResponseRedirect('/book/%s/' % book_for_sale.book.id)                                     
        else:
            messages.error(request, 'Purchase unsuccessful')
            return render(request, 'books/buy_form/buy.html', {'buy_form': buy_form(), 'book': book, 'book_for_sale': book_for_sale})
    else:
        return render(request, 'books/buy_form/buy.html', {'buy_form': buy_form(), 'book':book, 'book_for_sale': book_for_sale})
