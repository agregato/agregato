from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from agregato.feeds import LatestItemsFeed, WatchItemsFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^feeds/latest/$', LatestItemsFeed()),
    path('feeds/<int:watch_id>/', WatchItemsFeed()),
]
