from django.conf.urls import include, url
from .models import Book

def index(request):
    # two modules being displayed on top of page
    top_books = Book.objects.order_by('-rating')[:5]
    new_books = Book.objects.order_by('-year_published')[:5]

    # books for the genre selector
    genre = request.GET.get('genre') if request.GET.get('genre') is not None else 0
    genre_books = Book.objects.filter(genre=genre).order_by('-rating')[:5]
    genres = ['Science fiction','Drama', 'Action and Adventure','Romance','Mystery','Health','Children\'s','Science','History','Biographies']
    return render(request, 'books/homepage/index.html', {'top_books': top_books, 'new_books': new_books, 'book_by_genre' : genre_books, 'genres' : genres, 'genre': genres[int(genre)]})

