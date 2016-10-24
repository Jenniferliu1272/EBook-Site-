from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.contrib.auth.forms import UserCreationForm
from bookSell.forms import *
from bookSell.models import ourUser, Book, BookForSale
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def registerPage(request):
	def get(self, request):
		c = getStaticContext()
		c.update(csrf(request))
		c.update({'forms': [UserCreationForm(), registerationForm()]})
		return renderRegisterPage(c, request)
	def post(self, request):
		c = getStaticContext()
		c.update(csrf(request))
		session = request.session
		forms = request.POST
		userForm = UserCreationForm(forms)
		register = registrationForm(forms)
		user = userForm.save() # auth.User
		user.first_name = forms['first_name']
		user.last_name = forms['last_name']
		user.email = forms['email']
		user.save()
		c.update({'alert':1, 'message':'Successfully registered'})
		return renderLoginPage(c, request)
		
def renderRegisterPage(context, request):
    return render_to_response('books/homepage/book_list.html', context, RequestContext(request))
	
def renderLoginPage(context, request):
    return render_to_response('books/homepage/index.html', context, RequestContext(request))
