"""bookSell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blgo.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bookSell import views
import django.contrib.auth.views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^book/(?P<book_id>[0-9]+)/$', views.book, name='book'),
	url(r'^register/', views.register, name='register'),
	url(r'^login/', django.contrib.auth.views.login, name='login'),
	url(r'^logout/', django.contrib.auth.views.logout, name='logout'),
	url(r'^results/$', views.search, name='search'),
	url(r'^sell/$', views.sell_view, name='sell'),
	url(r'^genre/(?P<genre>.*)/$', views.genre, name='genre'),
    url(r'^book_rating/(?P<book_id>[0-9]+)/$', views.book_rating, name='book_rating'),


	#Sell Urls
	url(r'^sell/$', views.sell_view, name='sell'),
	url(r'^sell_results/', views.sell_search, name='sell_search'),
	url(r'sell_existing/(?P<book_id>[0-9]+)/(?P<back>.*)?', views.sell_existing, name="sell_existing"),
	url(r'^sell_original/', views.sell_original, name='sell_original'),

	#Buy Urls
	url(r'^buy/(?P<book_id>[0-9]+)', views.buy_book, name='buy_book'),
]  +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


