from django.conf.urls import include, url
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django import template

from bookSell.models import Book
from bookSell.constants import genres

def index(request):
    # three modules being displayed on top of page
	top_books = Book.objects.order_by('-year_published')[:5]
	new_books = Book.objects.order_by('-year_published')[:5]
	recommended_books = Book.objects.filter(genre=0).order_by('year_published')

    # books for the genre selector
	genre = request.GET.get('genre') if request.GET.get('genre') is not None else 0
	genre_books = Book.objects.filter(genre=genre).order_by('-year_published')[:5]
	return render(request, 'books/homepage/index.html', {'top_books': top_books, 'new_books': new_books, 'book_by_genre' : genre_books, 'genres' : genres, 'genre': genres[int(genre)], 'recommended_books':recommended_books})

