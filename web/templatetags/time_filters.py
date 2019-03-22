from django import template
from datetime import datetime

register = template.Library()

@register.filter
def is_past_time(time_str):
    now = int(datetime.now().strftime("%H%M"))
    current = int(time_str.replace(":",""))
    return (now > current)

@register.filter
def parse_date(date_string, format='%Y-%m-%dT%H:%M:%S+00:00'):
    """
    Return a datetime corresponding to date_string, parsed according to format.

    For example, to re-display a date string in another format::
        2019-03-21T13:30:00+00:00 

    """
    try:
        date_object = datetime.strptime(date_string, format)
        return date_object
    except ValueError:
        return None
