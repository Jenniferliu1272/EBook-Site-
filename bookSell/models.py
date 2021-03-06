from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from .constants import genres

import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()
    description = models.CharField(max_length=500)
    cover_image = models.ImageField(upload_to='cover_photos', blank=True, null=True)

    genreChoices = []
    for index, genre in enumerate(genres):
        genreChoices.append((index, genre))
    genre = models.IntegerField(
        choices=tuple(genreChoices)
    )

    def __str__(self):
        return self.title
    def _get_books_for_sale_count(self):
        books_for_sale = BookForSale.objects.filter(book=self.id,sold=False)
        return len(books_for_sale)

    def _average_rating(self):
        ratings = BookRating.objects.filter(book=self.id)
        return sum(r.rating for r in ratings) / len(ratings) if len(ratings) > 0 else 0

    books_for_sale_count = property(_get_books_for_sale_count)
    average_rating = property(_average_rating)
    def get_genre(self):
        if self.genre == 0:
            return "Science Fiction"
        elif self.genre == 1:
            return "Drama"
        elif self.genre == 2:
            return "Action and Adventure"
        elif self.genre == 3:
            return "Romance"
        elif self.genre == 4:
            return "Mystery"
        elif self.genre == 5:
            return "Health"
        elif self.genre == 6:
            return "Children's"
        elif self.genre == 7:
            return "Science"
        elif self.genre == 8:
            return "History"
        elif self.genre == 9:
            return "Biographies"

class BookForSale(models.Model):
    cost = models.IntegerField()
    sold = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    #Set to null for purpose of testing
    userSelling = models.ForeignKey(User, null=True, related_name="users_selling")
    userBought = models.ForeignKey(User, related_name="user_bought", blank=True, null=True)
    conditionChoices = (
        (0, 'Poor'),
        (1, 'Fair'),
        (2, 'Good'),
        (3, 'New'),
    )
    condition = models.IntegerField(
        choices=conditionChoices,
    )

    def _rating(self):
        return UserRating.objects.filter(book=self.id).first()
    
    rating = property(_rating) 

    def _seller_rating(self):
        ratings = UserRating.objects.filter(book__userSelling=self.userSelling.id)
        return sum(r.rating for r in ratings) / len(ratings) if len(ratings) > 0 else 0

    seller_rating = property(_seller_rating)
   
    def __str__(self):
        return self.book.title
        #+ " sold by " + self.userSelling.username
        #Will make adjustments once user login is available


class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

    # The additional attributes we wish to include.
	phone = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	
	genres_available = (
		(0, 'Science Fiction'),
		(1, 'Drama'),
		(2, 'Action and Adventure'),
		(3, 'Romance'),
		(4, 'Mystery'),
		(5, 'Health'),
		(6, 'Children'),
		(7, 'Science'),
		(8, 'History'),
		(9, 'Biographies')
	)
	favorite_genre = models.IntegerField(choices=genres_available)
	
	def _average_rating(self):
		return UserRating.objects.filter(BookForSale__UserSold=1)
        #return sum(r.rating for r in ratings) / len(ratings) if len(ratings) > 0 else 0

	average_rating = property(_average_rating)
    # Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

class Payment(models.Model):
    user = models.OneToOneField(User, null=True, related_name="user")
    credit_card = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    cvv = models.CharField(max_length=3, null=False)

    #Expiration Date
    year_dropdown = []
    for y in range(2016, (datetime.datetime.now().year + 5)):
        year_dropdown.append((y, y))
    year = models.IntegerField(choices=year_dropdown, default=datetime.datetime.now().year)

    month_dropdown = []
    month_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    for d in range(0, 12):
        month_dropdown.append((d, month_name[d]))
    month = models.IntegerField(choices=month_dropdown, default=datetime.datetime.now().month)

    #Billing Information
    street_address = models.CharField(max_length=150, default='', null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=10, null=False)
    postal = models.CharField(max_length=5, null=False)
    country = models.CharField(max_length=10, null=False)

    def __unicode__(self):
       return self.user.first_name + " " + self.user.last_name


class BookRating(models.Model):
    rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
     )
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.book.title + " " + self.user.firstname


class UserRating(models.Model):
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
     )
    comment = models.CharField(max_length=500)
    book = models.ForeignKey(BookForSale, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.book.book.title

class Wishlist(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    costLessThan = models.IntegerField(validators=[MinValueValidator(0)])
    conditionChoices = (
        (0, 'Poor'),
        (1, 'Fair'),
        (2, 'Good'),
        (3, 'New'),
    )
    betterConditionThan = models.IntegerField(
        choices=conditionChoices,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.book.title + " " + self.user.username
