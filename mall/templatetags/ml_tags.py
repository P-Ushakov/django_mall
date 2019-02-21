from django import template
from mall.models import TAG_DICT
from wagtail.core.models import Page

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
    tooltip = "ключевое слово"
    for key in TAG_DICT:
        symbol = TAG_DICT[key][0]
        dict_tooltip = TAG_DICT[key][1]
        if symbol == tag.name:
            tooltip = dict_tooltip
    return tooltip


@register.simple_tag
def ml_tag_header(tag=None):
    header = "ключевое слово"
    for key in TAG_DICT:
        symbol = TAG_DICT[key][0]
        dict_tooltip = TAG_DICT[key][1]
        if symbol == tag:
            header = dict_tooltip
    return header.capitalize()


#@register.inclusion_tag('ml_get_badges.html')(ml_get_badges)
def ml_get_badges(id=None):
    # take page id, returns list with of all descendants tags pairs ((key1,count1),(key2,count2),...)
    if id:
        ml_object = Page.objects.get(id=id)
        ml_descendants = ml_object.get_descendants()
        unique_tags = {}
        for descendant in ml_descendants:
            if hasattr(descendant.specific,  "auto_tags"):
                tags = descendant.specific.auto_tags.all()
                for tag in tags:
                    if tag.name in unique_tags:
                        unique_tags[tag.name] += 1
                    else:
                        unique_tags[tag.name] = 1
        if unique_tags:
            unique_tag_list = []
            for pair in unique_tags.items():
                unique_tag_list.append(pair)
            return {'unique_tag_list': unique_tag_list}


register.inclusion_tag('mall/ml_get_badges.html')(ml_get_badges)

