from django import forms
from bookSell.models import UserManager, ourUser, Book, BookForSale
from django.contrib.admin import widgets
from django.contrib.auth.models import User

class registerationForm(forms.ModelForm):
	class Meta:
		model = ourUser
		fields = ['first_name','last_name','email','phone']
	