from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='split')
@stringfilter
def split(value, key):
    print(value)
    return value.split(key)

@register.filter(name='split_timesince')
@stringfilter
def split_timesince(value, key):
    data = {
        'seconds': 'giây',
        'minutes': 'phút',
        'hours': 'giờ',
        'days': 'ngày',
        'weeks': 'tuần',
        'months': 'tháng',
        'years': 'năm',
        'second': 'giây',
        'minute': 'phút',
        'hour': 'giờ',
        'day': 'ngày',
        'week': 'tuần',
        'month': 'tháng',
        'year': 'năm',
    }
    
    value = value.split(key)[0]

    for key in data.keys():
        value = value.replace(key, data[key])
    
    return f"{value} trước"
