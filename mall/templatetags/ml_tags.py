from django import template
from mall.models import TAG_DICT

register = template.Library()


@register.simple_tag
def ml_tag_border(tag=None):
    button_color = "success"
    for key in TAG_DICT:
        symbol = TAG_DICT[key][0]
        color = TAG_DICT[key][2]
        if symbol == tag.name:
            button_color = color
    return button_color

@register.simple_tag
def ml_tag_tooltip(tag=None):
    tooltip = ""
    for key in TAG_DICT:
        symbol = TAG_DICT[key][0]
        dict_tooltip = TAG_DICT[key][1]
        if symbol == tag.name:
            tooltip = dict_tooltip
    return tooltip
