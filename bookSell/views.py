from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import ourUser, Book, BookForSale
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # two modules being displayed on top of page
    top_books = Book.objects.order_by('-rating')[:5]
    new_books = Book.objects.order_by('-year_published')[:5]

    # books for the genre selector
    genre = request.GET.get('genre') if request.GET.get('genre') is not None else 0
    genre_books = Book.objects.filter(genre=genre).order_by('-rating')[:5]
    genres = ['Science fiction','Drama', 'Action and Adventure','Romance','Mystery','Health','Children\'s','Science','History','Biographies']
    return render(request, 'books/homepage/index.html', {'top_books': top_books, 'new_books': new_books, 'book_by_genre' : genre_books, 'genres' : genres, 'genre': genres[int(genre)]})


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
	
def registerPage(request):
	def get(self, request):
		c = getStaticContext()
		c.update(csrf(request))
		c.update({'forms': [UserCreationForm(), registerationForm()]})
		return renderRegisterPage(c, request)
	def post(self, request):
		c = getStaticContext()
		c.update(csrf(request))
		session = request.session
		forms = request.POST
		userForm = UserCreationForm(forms)
		register = registrationForm(forms)
		user = userForm.save() # auth.User
		user.first_name = forms['first_name']
		user.last_name = forms['last_name']
		user.email = forms['email']
		user.save()
		c.update({'alert':1, 'message':'Successfully registered'})
		return renderLoginPage(c, request)
		
def renderRegisterPage(context, request):
    return render_to_response('books/homepage/book_list.html', context, RequestContext(request))
	
def renderLoginPage(context, request):
    return render_to_response('books/homepage/index.html', context, RequestContext(request))
