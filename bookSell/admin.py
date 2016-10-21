from django.contrib import admin
from .models import Book, BookForSale

admin.site.register(Book)
admin.site.register(BookForSale)

