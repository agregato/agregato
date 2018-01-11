from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from agregato.feeds import LatestEntriesFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^feed/latest/', LatestEntriesFeed()),
]
