from django.contrib.syndication.views import Feed
from agregato.models import Item


class LatestEntriesFeed(Feed):
    title = "All Items"
    link = "/sitenews/"
    description = "All Recent Items"

    def items(self):
        return Item.objects.order_by('-add_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.href
