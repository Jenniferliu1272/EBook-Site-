from django.http import HttpResponse
from .models import Book

def index(request):
	latest_book_list = Book.objects.order_by('-pub_date')[:5]
	output = ', '.join([q.title for q in latest_book_list])
	return HttpResponse(output)
