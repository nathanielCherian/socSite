from django import template
from django.utils.safestring import mark_safe
import datetime
from dateutil.parser import parse
from django.utils import timezone
from markdown import markdown


from soc_site.settings import (
    MARKDOWNX_MARKDOWN_EXTENSIONS,
    MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
)

register = template.Library()


@register.filter(name='past_time', expects_localtime=True)
def past_time_parse(text):
    t = text
    now = timezone.now()
    difference = (now - text).total_seconds()

    duration = datetime.timedelta(seconds=difference)

    days, seconds = duration.days, duration.seconds

    if days > 365:
        return mark_safe(f"{int(days/365)} year(s) ago")

    if days > 0:
        return mark_safe(f"{days} day(s) ago")
    
    if seconds >= 3600:
        return mark_safe(f"{int(seconds/3600)} hour(s) ago")

    if seconds >= 60:
        return mark_safe(f"{int(seconds/60)} minute(s) ago")

    return mark_safe(f"{seconds} second(s) ago")



@register.filter(name='in_queue')
def get_in_queue(notifications):
    return notifications.filter(noti_que=True)



@register.filter(name='get_votes')
def get_votes(object_, user):

    votes = object_.votes.filter(user=user)

    if votes:
        return votes.first().family
    else:
        return None


@register.filter(name='get_upvotes')
def get_upvotes(object_):
    votes = object_.votes.filter(family=True)
    return votes

@register.filter(name='get_downvotes')
def get_downvotes(object_):
    votes = object_.votes.filter(family=False)
    return votes


@register.filter(name='to_HTML')
def markdown_to_HTML(content):

    md = markdown(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)

    return md