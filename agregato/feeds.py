from django.contrib.syndication.views import Feed
from agregato.models import Item, Watch


class LatestItemsFeed(Feed):
    title = "All Items"
    description = "All Recent Items"
    link = '/cipa/'

    def items(self):
        return Item.objects.order_by('-add_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:255] + '...'

    def item_link(self, item):
        return item.href


class WatchItemsFeed(LatestItemsFeed):
    title = "Watch Items"
    description = "Watch Recent Items"
    link = '/dupa/'

    def get_object(self, request, watch_id):
        return Watch.objects.get(pk=watch_id)

    def items(self, watch):
        return Item.objects.filter(watch=watch).order_by('-add_date')[:10]
