from django.conf.urls import include, url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from bookSell.models import *
from bookSell.forms import *
from django.db.models import Q
from bookSell.constants import genres, conditions
from django.contrib import messages


def buy_book(request, book_id):
    if request.user.is_authenticated():
        book = Book.objects.get(id=book_id)
        exist = False
        try:
            user = Payment.objects.get(user=request.user)
            buying_form = buy_form(instance=user)
            exist = True
        except Payment.DoesNotExist:
            buying_form = buy_form()

        if request.method == 'POST':
            if exist is False:
                buying_form = buy_form(request.POST)
            else:
                buying_form = buy_form(request.POST, instance=Payment.objects.get(user=request.user))
            if buying_form.is_valid():
                if exist is False:
                    buying_form.save_buyForm(user_buying=request.user)
                else:
                    buying_form.save()

                book_for_sale = BookForSale.objects.get(id=book_id)
                book_for_sale.userBought = request.user
                book_for_sale.sold = True
                book_for_sale.save()
                return render(request, 'books/buy_form/buy_confirm.html', {'buy_form': buying_form, 'book': book, 'book_for_sale': book_for_sale})
            else:
                return render(request, 'books/buy_form/buy.html', {'buy_form': buy_form(), 'book': book})
        else:
            return render(request, 'books/buy_form/buy.html', {'buy_form': buying_form, 'book': book})
    else:
        return redirect('../')
