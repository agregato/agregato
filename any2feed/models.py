from django.db import models
from django.utils.translation import ugettext_lazy as _


class Item(models.Model):
    watch = models.ForeignKey('Watch', verbose_name=_(u"watch"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_(u"title"), blank=True, null=True)
    href = models.CharField(max_length=255, verbose_name=_(u"href"), blank=True, null=True)
    content = models.TextField(verbose_name=_(u"content"), blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_(u"add_date"))

    class Meta:
        verbose_name = _(u"item")
        verbose_name_plural = _(u"items")
        ordering = ['-add_date']
        get_latest_by = 'add_date'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.href


class FieldInstance(models.Model):
    item = models.ForeignKey('Item', verbose_name=_(u"item"), related_name="fields", on_delete=models.CASCADE)
    definition = models.ForeignKey('FieldDefinition', verbose_name=_(u"field definition"), on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name=_(u"content"))

    class Meta:
        verbose_name = _(u"field instance")
        verbose_name_plural = _(u"field instances")

    def __unicode__(self):
        return self.content


class FieldDefinition(models.Model):
    watch = models.ForeignKey('Watch', verbose_name=_(u"watch"), related_name="fields", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_(u"title"))
    regexp = models.CharField(max_length=255, verbose_name=_(u"regexp"), blank=True, null=True)
    xpath = models.CharField(max_length=255, verbose_name=_(u"xpath"), blank=True, null=True)

    class Meta:
        verbose_name = _(u"field definition")
        verbose_name_plural = _(u"field definitions")

    def __unicode__(self):
        return self.title


class Watch(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_(u"user"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_(u"title"))
    title_regexp = models.CharField(max_length=255, verbose_name=_(u"title regexp"), blank=True, null=True)
    title_xpath = models.CharField(max_length=255, verbose_name=_(u"title xpath"), blank=True, null=True)
    content_regexp = models.CharField(max_length=255, verbose_name=_(u"content regexp"), blank=True, null=True)
    content_xpath = models.CharField(max_length=255, verbose_name=_(u"content xpath"), blank=True, null=True)
    href_regexp = models.CharField(max_length=255, verbose_name=_(u"href regexp"), blank=True, null=True)
    href_xpath = models.CharField(max_length=255, verbose_name=_(u"href xpath"), blank=True, null=True)
    url = models.CharField(max_length=255, verbose_name=_(u"url"))
    notify = models.CharField(max_length=255, blank=True, verbose_name=_(u"notify"))

    class Meta:
        verbose_name = _(u"watch")
        verbose_name_plural = _(u"watches")

    def __unicode__(self):
        return self.title


class Filter(models.Model):

    watch = models.ForeignKey('Watch', verbose_name=_(u"watch"), related_name='filters', on_delete=models.CASCADE)
    regexp = models.CharField(max_length=255, verbose_name=_(u"regexp"))

    class Meta:
        verbose_name = _(u"filter")
        verbose_name_plural = _(u"filters")

    def __unicode__(self):
        return self.regexp
