from django.contrib import admin
from .models import Book, UserProfile, BookForSale, BookRating, UserRating

admin.site.register(Book)
admin.site.register(BookForSale)
admin.site.register(UserProfile)
admin.site.register(BookRating)
admin.site.register(UserRating)