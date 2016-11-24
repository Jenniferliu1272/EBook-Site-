from django.contrib import admin
from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Book)
admin.site.register(BookForSale)
admin.site.register(UserProfile)
admin.site.register(BookRating)
admin.site.register(UserRating)
admin.site.register(Wishlist)
admin.site.register(Payment, PaymentAdmin)


