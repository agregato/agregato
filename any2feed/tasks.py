import datetime
import re
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from django.conf import settings
from django.template import loader
from lxml import html

from .models import FieldInstance, Item, Watch


def get_item(watch, element):
    content = element.text_content().strip()

    if "google_ad_client" in content:
        return

    filters_passed = True
    for filter in watch.filters.all():
        if not re.findall(filter.regexp, content, re.IGNORECASE):
            filters_passed = False

    if not filters_passed:
        return

    try:
        title = element.find(watch.title_xpath).text_content().strip()
    except AttributeError:
        return

    href = element.find(watch.href_xpath).attrib.get('href')
    if href.startswith('/'):
        href = "http://{}{}".format(watch.url.lstrip('http://').split('/')[0], href)
    elif not href.startswith('http'):
        href = "http://{}{}".format(watch.url.lstrip('http://'), href)

    fields = []
    for field in watch.fields.all():
        if field.xpath:
            field_element = element.find(field.xpath)
            if field_element is not None:
                field_content = field_element.text_content().strip()
                if content:
                    fields.append({'definition': field, 'content': field_content})

    return {'title': title, 'href': href, 'content': content, 'fields': fields}


def get_items_for_watch(watch):
    """
    Gets items from given url.

    Returns dictionary containing title, href and content
    """
    root = html.fromstring(requests.get(watch.url).text)
    if watch.content_xpath:
        elements = root.findall(watch.content_xpath)
        for element in elements:
            item = get_item(watch, element)
            if item:
                yield item

    elif watch.content_regexp:
        raise NotImplemented("jeszcze nie da sie regexpem, tylko xpath")
    else:
        raise Exception("nie podany regexp ani xpath")


def create_item(watch, title, href, content, fields=None):
    """
    Creates `Item` and saves it.

    Returns saved item.
    """

    item = Item()
    item.watch = watch
    item.title = title
    item.href = href
    item.content = content
    item.save()
    if fields:
        for field in fields:
            fi = FieldInstance()
            fi.definition = field['definition']
            fi.content = field['content']
            fi.item = item
            fi.save()

    return item


def create_items(watch, items):
    """
    Returns generator with created `Item` object.
    """
    for item in items:
        exists = Item.objects.filter(watch=watch, href=item['href']).exists()
        if not exists:
            yield create_item(watch, **item)


def fetch_items(watch):
    """
    Fetches `Item` objects for given watch.

    Saves them if `save` is set to `True`.
    """
    raw_items = get_items_for_watch(watch)
    return create_items(watch, raw_items)


def make_items(watch):
    items = list(fetch_items(watch))
    if watch.notify and items:
        send_notification(watch, watch.user, items)


def check_watches():
    watches = Watch.objects.all()
    for watch in watches:
        make_items(watch)


def send_notification(watch, user, items):
    html_template = loader.get_template('any2feed/email_notification.html')
    plain_template = loader.get_template('any2feed/email_notification.txt')
    context = {
        'user': user,
        'items': items,
    }
    html = html_template.render(context)
    plain = plain_template.render(context)

    me = settings.EMAIL_FROM
    you = watch.notify

    for you in watch.notify.split(','):
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
