from django import template
from mall.models import MlObjectPage
from wagtail.core.models import Page

register = template.Library()


@register.simple_tag
def ml_obj_tag_border(tag=None):
    button_color = "success"
    for key in MlObjectPage.tag_dict:
        symbol = MlObjectPage.tag_dict[key][0]
        color = MlObjectPage.tag_dict[key][2]
        if hasattr(tag, 'name'):
            if symbol == tag.name:
                button_color = color
        else:
            if symbol == tag:
                button_color = color

    return button_color


@register.simple_tag
def ml_obj_tag_tooltip(tag=None):
    tooltip = "ключевое слово"
    for key in MlObjectPage.tag_dict:
        symbol = MlObjectPage.tag_dict[key][0]
        dict_tooltip = MlObjectPage.tag_dict[key][1]
        if hasattr(tag, 'name'):
            if symbol == tag.name:
                tooltip = dict_tooltip
        else:
            if symbol == tag:
                tooltip = dict_tooltip
    return tooltip


@register.simple_tag
def ml_obj_tag_header(tag=None):
    header = "ключевое слово"
    for key in MlObjectPage.tag_dict:
        symbol = MlObjectPage.tag_dict[key][0]
        dict_tooltip = MlObjectPage.tag_dict[key][1]
        if symbol == tag:
            header = dict_tooltip
    return header.capitalize()


# FixMe deprecated
def collect_unique_tag(page):
    # accept Page, return dictionary of unique tags
    unique_tags = {}
    ml_descendants = page.get_descendants().live()
    for descendant in ml_descendants:
        if hasattr(descendant.specific, "auto_tags"):
            tags = descendant.specific.auto_tags.all()
            for tag in tags:
                if tag.name in unique_tags:
                    unique_tags[tag.name] += 1
                else:
                    unique_tags[tag.name] = 1
    return unique_tags


def ml_obj_collect_status(page, *args, **kwargs):
    descendants = page.get_descendants().exact_type(MlObjectPage).live()
    statuses = {}
    for descendant in descendants:
        for item in args:
            if hasattr(descendant.specific, item):
                if item in statuses:
                    statuses[item] += int(getattr(descendant.specific, item))
                else:
                    statuses[item] = int(getattr(descendant.specific, item))
    for item in args:
        if hasattr(page.specific, item):
            setattr(page.specific, item, statuses[item])
    super(Page, page.specific).save()
    return statuses


def ml_obj_get_badges(id=None):
    # take page id, returns list with of all descendants tags pairs ((key1,count1),(key2,count2),...)
    if id:
        ml_object = Page.objects.get(id=id)

        unique_tag_list = []
        unique_tags = {}
        status_args = ('status_ok', 'status_bad', 'is_enabled', 'is_disabled', 'diagnosed',
                       'have_to_be_diagnosed', 'need_service', 'have_maintenance', 'is_critical',
                       'call_down', 'have_to_be_repaired', 'is_critically_broken')
        statuses = ml_obj_collect_status(ml_object, *status_args)

        for key, value in statuses.items():
            if (key in MlObjectPage.tag_dict) and value > 0:
                unique_tags[MlObjectPage.tag_dict[key][0]] = value


        # update_cashed_ml_object_page_tags = True
        # partial cache reset
        # ml_descendants = ml_object.get_descendants().exact_type(MlObjectPage).live()
        # full cache reset

        if unique_tags:
            unique_tag_list = []
            for pair in unique_tags.items():
                unique_tag_list.append(pair)

        return {'unique_tag_list': unique_tag_list, 'id': id}


register.inclusion_tag('mall/ml_get_badges.html')(ml_obj_get_badges)

