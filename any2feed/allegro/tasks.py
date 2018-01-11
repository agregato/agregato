
import json
import urllib

from lxml import html

from django.core.files.base import ContentFile

from .models import Item, AllegroWatch


def get_items_from_allegro(url):
    """
    Gets items from given url.

    Returns dictionary containing allegro_id, title, price, href and image_url
    """
    root = html.fromstring(unicode(urllib.urlopen(url).read(), 'utf-8'))
    elements = root.findall('body/div[@id="wrapper"]/div/div[@id="listing"]/section/article')
    for element in elements:
        allegro_id = element.attrib.get('data-id')
        title = element.find('div/div[3]/header/h2/a/span').text
        price = element.find("div/div[2]/div").text_content()
        href = element.find('div/div[3]/header/h2/a').attrib.get('href')
        if href.startswith('/'):
            href = "http://{}{}".format(url.lstrip('http://').split('/')[0], href)
        try:
            image_url = json.loads(element.find('div/div[1]').attrib.get('data-img'))[0][2]
        except IndexError:
            image_url = None

        yield {'title': title, 'allegro_id': allegro_id, 'price': price, 'href': href, 'image_url': image_url}


def create_item(watch, allegro_id, title, price, href, image_url, save=False):
    """
    Creates `Item` and saves it.

    Returns saved item.
    """

    item = Item()
    item.watch = watch
    item.allegro_id = allegro_id
    item.title = title
    item.price = price.strip()
    item.href = href
    item.image_url = image_url
    item.image.save(allegro_id + '.jpg', ContentFile(urllib.urlopen(image_url).read()))
    if save:
        item.save()

    return item


def create_items(watch, items, save=False):
    """
    Returns generator with created `Item` object.
    """
    for item in items:
        exists = Item.objects.filter(watch=watch, allegro_id=item['allegro_id']).exists()
        if not exists:
            yield create_item(watch, save=save, **item)


def fetch_items(watch, save=False):
    """
    Fetches `Item` objects for given watch.

    Saves them if `save` is set to `True`.
    """
    raw_items = get_items_from_allegro(watch.url)
    return create_items(watch, raw_items, save)


def make_items(watch):
    items = list(fetch_items(watch, save=True))
    if watch.notify and items:
        send_notification(watch, watch.user, items)


def check_watches():
    watches = AllegroWatch.objects.all()
    for watch in watches:
        make_items(watch)


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import Context, loader
from django.conf import settings
import datetime
from email.header import Header


def send_notification(watch, user, items):
    html_template = loader.get_template('allegro/email_notification.html')
    plain_template = loader.get_template('allegro/email_notification.txt')
    context = Context({
        'user': user,
        'items': items,
    })
    html = html_template.render(context)
    plain = plain_template.render(context)

    me = settings.EMAIL_FROM
    you = user.email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(u"{} - {}".format(datetime.datetime.now(), watch.title).encode('utf8'), 'utf8')
    msg['From'] = me
    msg['To'] = you

    part1 = MIMEText(plain.encode('utf8'), 'plain', 'utf8')
    part2 = MIMEText(html.encode('utf8'), 'html', 'utf8')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('%s:%s' % (settings.EMAIL_HOST, str(settings.EMAIL_PORT)))
    if settings.EMAIL_USE_TLS:
        s.starttls()
    s.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
    s.sendmail(me, you, msg.as_string())
    s.quit()


def delete_old(delta=3600):
    older_than = datetime.datetime.now() - datetime.timedelta(seconds=delta)
    map(Item.delete, Item.objects.filter(add_date__lte=older_than))
