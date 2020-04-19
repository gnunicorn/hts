from django import template
from django.conf import settings
import random

register = template.Library()

@register.simple_tag
def random_bubble_path():
    return random.choice(settings.BUBBLES)
