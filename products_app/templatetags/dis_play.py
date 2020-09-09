from django import template
from home_app.models import Translation
import re

register = template.Library()

"""
Template tags to define a variable and to add a number to a variable not using |add only usable 
for a display {{toto|add}}
used in detail_view
"""


@register.simple_tag(takes_context=True)
def dis_play(context, value):
    try:
        language = context.request.session['language']
    except KeyError:
        language = "UK"
    text_to_display = Translation.get_translation(value, language)
    return text_to_display

@register.filter
def get_error_msg(value):
    value = str(value)
    print(value)
    pattern = "<li>(.*?)</li>"
    print(value)
    try:
        newvalue = re.search(pattern, value).group(1)
    except AttributeError:
        newvalue = re.search(pattern, value)
    return newvalue
