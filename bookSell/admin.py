from django.contrib import admin
from .models import Book, UserProfile, BookForSale

admin.site.register(Book)
admin.site.register(BookForSale)
admin.site.register(UserProfile)