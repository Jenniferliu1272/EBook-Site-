from django import forms
from bookSell.models import *

from django.contrib.admin import widgets
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'phone']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update({'class': 'form-control'})
        self.fields['lastname'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})

class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['comment', 'user', 'book', 'rating']

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['comment', 'book', 'rating']


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

    def save_sellFormExisiting(self, book_id, user, commit=True):
        current_book = super(sell_form_existing, self).save(commit=False)
        current_book.userSelling = user
        current_book.book = Book.objects.get(id=book_id)
        current_book.condition = self.cleaned_data['condition']
        current_book.cost = self.cleaned_data['cost']

        if commit:
            current_book.save()
        return current_book

class sell_form_original(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year_published', 'genre', 'cover_image']

    def __init__(self, *args, **kwargs):
        super(sell_form_original, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_published'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['cover_image'].widget.attrs.update({'class': 'form-control'})

    def save_sellFormOriginal(self, commit=True):
        new_book = super(sell_form_original, self).save(commit=False)
        new_book.title = self.cleaned_data['title']
        new_book.author = self.cleaned_data['author']
        new_book.description = self.cleaned_data['description']
        new_book.year_published = self.cleaned_data['year_published']
        new_book.genre = self.cleaned_data['genre']
        new_book.cover_image = self.cleaned_data['cover_image']

        new_book = Book(title=new_book.title, author=new_book.author, description=new_book.description,
                        year_published=new_book.year_published, genre=new_book.genre, cover_image=new_book.cover_image)
        new_book.save()

        if commit:
            new_book.save()
        return new_book

"Forms for buying a book"

class buy_form(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['credit_card', 'first_name','last_name','cvv','street_address','city','state','postal', 'country', 'year', 'month']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(buy_form, self).__init__(*args, **kwargs)
        self.fields['month'].widget.attrs.update({'class': 'btn btn-primary'})
        self.fields['year'].widget.attrs.update({'class': 'btn btn-primary'})

    def save_buyForm(self, user_buying, commit=True):
        new = super(buy_form, self).save(commit=False)
        if new.user is None:
            new.user = user_buying

        if commit:
            new.save()
        return new
