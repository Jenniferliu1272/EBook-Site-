from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()
    description = models.CharField(max_length=500)
    rating = models.IntegerField()

    genreChoices = (
		(0, 'Science fiction'),
		(1, 'Drama'),
		(2, 'Action and Adventure'),
		(3, 'Romance'),
		(4, 'Mystery'),
		(5, 'Health'),
		(6, 'Children\'s'),
		(7, 'Science'),
		(8, 'History'),
		(9, 'Biographies')
    	)

    genre = models.IntegerField(
        max_length=1,
        choices=genreChoices,
		default=0
    )

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
        (0, 'Poor'),
        (1, 'Fair'),
        (2, 'Good'),
        (3, 'New'),
    )
    condition = models.IntegerField(
        max_length=1,
        choices=conditionChoices,
    )

    def __str__(self):
    	return self.book.title + " sold by " + self.userSelling.username

class UserManager(models.Manager):
    def register(self, userName, password, fname, lname, email, phone):
        
		user = User.objects.create_user(username=userName, password=password, email=email, first_name=fname, last_name=lname, phone=phone)
		ourUser = ourUser(user=user)
		user.ourUser = ourUser
		return user
		
    def login(self, userName, password, request=None):
        user = authenticate(username=userName, password=password)
        # global namespace auth login
        if request != None:
			login(request, user)
        return user

class ourUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='ourUser')
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	phone = models.CharField(max_length=30)
	
	def __str__(self):
		s =  "%s %s\n" % (self.user.first_name, self.user.last_name)
		return s

