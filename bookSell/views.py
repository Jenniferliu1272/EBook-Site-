from django.http import HttpResponse
from django.template import loader

from .models import Book

def index(request):
    top_books = Book.objects.order_by('rating')[:5]
    template = loader.get_template('books/index.html')
    context = {
        'top_books': top_books,
    }
    return HttpResponse(template.render(context, request))

def bookPage(request, book_id):
    return HttpResponse("You're looking at book %s." % book_id)

def userPage(request, user_id):
    return HttpResponse("You're looking at user %s." % user_id)
