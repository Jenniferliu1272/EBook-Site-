from django.contrib import admin
from .models import Book, ourUser, BookForSale

admin.site.register(Book)
admin.site.register(BookForSale)
admin.site.register(ourUser)