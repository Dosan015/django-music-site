from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def insert_mark(context, obj):
    string = str(obj)
    mark = context['last_question']
    low_string = string.lower()
    low_mark = mark.lower()
    if low_string.find(low_mark) != -1:
        index = low_string.find(low_mark)
        m = len(mark)
        mark_orginal = string[index:index+m]
        string = string[:index]+'<mark>'+mark_orginal+'</mark>'+string[index+m:]
    return mark_safe(string)
