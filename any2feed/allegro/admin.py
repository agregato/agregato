from django.contrib import admin

from .models import AllegroWatch, Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'add_date', 'price', 'display_image')

    def display_image(self, obj):
        if obj.image_url:
            return "<img src=\"%s\" />" % obj.image_url
        else:
            return "no image"
    display_image.allow_tags = True
    display_image.short_description = "image"


admin.site.register(Item, ItemAdmin)
admin.site.register((AllegroWatch,))
