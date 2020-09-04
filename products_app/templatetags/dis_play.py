from django import template
from home_app.models import Translation

register = template.Library()

"""
Template tags to define a variable and to add a number to a variable not using |add only usable 
for a display {{toto|add}}
used in detail_view
"""


@register.simple_tag(takes_context=True)
def dis_play(context, value):
    language = context.request.session['language']
    text_to_display = Translation.get_translation(value, language)
    return text_to_display
