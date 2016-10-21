from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()
    description = models.CharField(max_length=500)
    rating = models.IntegerField()
    def __str__(self):
    	return self.title

    def _get_books_for_sale_count(self):
    	return len(BookForSale.objects.filter(book=self.id))
    books_for_sale_count = property(_get_books_for_sale_count)


class BookForSale(models.Model):
    cost = models.IntegerField()
    sold = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    userSelling = models.ForeignKey(User, related_name="users_selling")
    userBought = models.ForeignKey(User, related_name="user_bought", blank=True, null=True)
    conditionChoices = (
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('new', 'New'),
    )
    condition = models.CharField(
        max_length=4,
        choices=conditionChoices,
    )

    def __str__(self):
    	return self.book.title + " sold by " + self.userSelling.username



