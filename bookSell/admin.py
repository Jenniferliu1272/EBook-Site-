from django.contrib import admin
from .models import Book, User, BookForSale

admin.site.register(Book)
admin.site.register(User)
admin.site.register(BookForSale)