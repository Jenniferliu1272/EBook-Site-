from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()
    description = models.CharField(max_length = 500)
    rating = models.IntegerField()
    def __str__(self):
		return self.title


class User(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phoneNumber = models.IntegerField()

class BookForSale(models.Model):
	cost = models.IntegerField()
	sold = models.BooleanField(default=False)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	userSelling = models.ForeignKey(User, related_name="users_selling")
	userBought = models.ForeignKey(User, related_name="user_bought", blank=True, null=True)


