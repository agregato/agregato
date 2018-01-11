from django.contrib import admin

from .models import Watch, Item, FieldDefinition, FieldInstance, Filter


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = FieldDefinition


class FieldInstanceInlineAdmin(admin.TabularInline):
    model = FieldInstance


class FilterInlineAdmin(admin.TabularInline):
    model = Filter


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'add_date', 'content', 'fields_content')

    """
    def display_image(self, obj):
        if obj.image:
            return "<img src=\"%s\" />" % get_image(obj.image, ResizedImage.MODE_ZOOM, 240, 160)
        else:
            return "no image"
    display_image.allow_tags = True
    display_image.short_description = "image"
    """
    inlines = [FieldInstanceInlineAdmin]

    list_filter = ['watch']
    list_select_related = True

    def fields_content(self, obj):
        ret = u"<dl>"
        for field in obj.fields.all():
            ret += u"<dt>{}</dt><dd>{}</dd>".format(field.definition.title, field.content)
        ret += u"</dl>"
        return ret
    fields_content.allow_tags = True
    fields_content.short_description = "Fields"


class WatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    inlines = [FieldDefinitionInlineAdmin, FilterInlineAdmin]
    save_as = True


admin.site.register(Item, ItemAdmin)
admin.site.register(Watch, WatchAdmin)
