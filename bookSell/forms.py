from django import forms
from bookSell.models import *

from django.contrib.admin import widgets
from django.contrib.auth.models import User

class registerationForm(forms.ModelForm):
	class Meta:
		model = ourUser
		fields = ['first_name','last_name','email','phone']

class sell_book_form_p1(forms.ModelForm):
    class Meta:
        model = sellBookForm
        exclude = ('rating', 'genre', 'cost', 'condition',)
        fields = ['title','author','description','year_published']

    def __init__(self, *args, **kwargs):
        super(sell_book_form_p1, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_published'].widget.attrs.update({'class': 'form-control'})

    def save_sell_form_p1(self):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        description = self.cleaned_data['description']
        year_published = self.cleaned_data['year_published']
        """cost = self.cleaned_data['cost']"""
        """condition = self.cleaned_data['condition']"""

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



