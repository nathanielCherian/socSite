from django import template
from django.utils.safestring import mark_safe
import datetime
from dateutil.parser import parse
from django.utils import timezone

register = template.Library()


@register.filter(name='past_time', expects_localtime=True)
def past_time_parse(text):
    t = text
    now = timezone.now()
    difference = (now - text).total_seconds()
    #dt = parse(text)
    #date = datetime.datetime.strptime(str(text), '%Y-%m-%d %H:%M:%S')
    return mark_safe(f"{difference}")