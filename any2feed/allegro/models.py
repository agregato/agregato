from django.db import models
from django.utils.translation import ugettext_lazy as _


class Item(models.Model):
    watch = models.ForeignKey('AllegroWatch', verbose_name=_(u"watch"), on_delete=models.CASCADE)
    allegro_id = models.CharField(max_length=255, verbose_name=_(u"allegro id"))
    title = models.CharField(max_length=255, verbose_name=_(u"title"))
    price = models.CharField(max_length=255, verbose_name=_(u"price"))
    href = models.CharField(max_length=255, verbose_name=_(u"href"))
    image_url = models.CharField(max_length=255, verbose_name=_(u"allegro image"))
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_(u"add_date"))

    class Meta:
        verbose_name = _(u"item")
        verbose_name_plural = _(u"items")
        ordering = ['-add_date']
        get_latest_by = 'add_date'
        unique_together = [['watch', 'allegro_id']]

    def __unicode__(self):
        return self.title


class AllegroWatch(models.Model):

    user = models.ForeignKey('auth.User', verbose_name=_(u"user"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_(u"title"))
    url = models.CharField(max_length=255, verbose_name=_(u"url"))
    notify = models.BooleanField(default=False, verbose_name=_(u"notify"))

    class Meta:
        verbose_name = _(u"allegro watch")
        verbose_name_plural = _(u"allegro watches")

    def __unicode__(self):
        return self.title
