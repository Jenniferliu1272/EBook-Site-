from django import forms
from bookSell.models import *

from django.contrib.admin import widgets
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["rating"]

"""
Form for selling a book that already exist in the
database
"""
class sell_form_existing(forms.ModelForm):
    class Meta:
        model = BookForSale
        fields = ['cost', 'condition']
        #Currently used as stub
        exclude = ['userSelling', 'sold']

    def __init__(self, *args, **kwargs):
        super(sell_form_existing, self).__init__(*args, **kwargs)
        self.fields['cost'].widget.attrs.update({'class': 'form-control'})
        self.fields['condition'].widget.attrs.update({'class': 'form-control'})

    def save_sellFormExisiting(self, book_id, commit=True):
        current_book = super(sell_form_existing, self).save(commit=False)
        current_book.book = Book.objects.get(id=book_id)
        current_book.condition = self.cleaned_data['condition']
        current_book.cost = self.cleaned_data['cost']

        if commit:
            current_book.save()
        return current_book

class sell_form_original(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year_published', 'rating', 'genre']

    def __init__(self, *args, **kwargs):
        super(sell_form_original, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_published'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    def save_sellFormOriginal(self, commit=True):
        new_book = super(sell_form_original, self).save(commit=False)
        new_book.title = self.cleaned_data['title']
        new_book.author = self.cleaned_data['author']
        new_book.description = self.cleaned_data['description']
        new_book.year_published = self.cleaned_data['year_published']
        new_book.rating = self.cleaned_data['rating']
        new_book.genre = self.cleaned_data['genre']

        new_book = Book(title=new_book.title, author=new_book.author, description=new_book.description,
                        year_published=new_book.year_published, rating=new_book.rating, genre=new_book.genre)
        new_book.save()

        if commit:
            new_book.save()
        return new_book












"""class sell_book_form_p1(forms.ModelForm):
    class Meta:
        model = Book
        #exclude = ('title','author','description','year_published')
        fields = ['title', 'author', 'description', 'year_published', 'rating', 'genre']

    def __init__(self, *args, **kwargs):
        super(sell_book_form_p1, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_published'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})

    def save_sell_form_p1(self):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        description = self.cleaned_data['description']
        year_published = self.cleaned_data['year_published']
        cost = self.cleaned_data['cost']
        condition = self.cleaned_data['condition']

        new_book = Book(title=title, author=author, description=description,
                        year_published=year_published, rating=2, genre=0)
        new_book.save()

        return new_book


class sell_book_form_p2(forms.ModelForm):
    class Meta:
        model = sellBookForm
        exclude = ('title','author','description','year_published',)
        fields = ['rating', 'genre', 'cost', 'condition']

    def __init__(self, *args, **kwargs):
        super(sell_book_form_p2, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control'})
        self.fields['condition'].widget.attrs.update({'class': 'form-control'})

    def save_sell_form_p2(self, book_id):
        rating = self.cleaned_data['rating']
        genre = self.cleaned_data['genre']
        cost = self.cleaned_data['cost']
        condition = self.cleaned_data['condition']

        current_book = Book.objects.get(id=book_id)
        current_book.rating = rating
        current_book.genre = genre
        current_book.condition = condition
        current_book.cost = cost
        current_book.save()

        return current_book
"""


