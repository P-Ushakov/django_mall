# Wagtail models (inherited  from page)

# django core modules
from django.db import models

# Wagtail modules
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.search import index

# other modules
from datetime import datetime
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


# Mall object list
class MlObjectIndexPage(Page):
    intro = models.TextField(verbose_name='краткое описание',
                             blank=True)

    # overriding default get_context to include only live objects, ordered by title
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # can be ordered by published date: order_by('-first_published_at')
        ml_objects = self.get_children().live().order_by('title')
        context['ml_objects'] = ml_objects
        return context

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License'),
    ]

    class Meta:
        verbose_name = "список объектов"
        verbose_name_plural = "список объектов"


# Mall object tag
class MlObjectTag(TaggedItemBase):
    content_object = ParentalKey(
        'MlObjectPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "ключ поиска"
        verbose_name_plural = "ключи поиска"


# List of tags
class MlObjectTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):

        # Filter by tag
        tag = request.GET.get('tag')
        ml_objects = MlObjectPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['ml_objects'] = ml_objects
        return context


# Mall object
class MlObjectPage(Page):
    buy_date = models.DateField("дата приобретения", blank=True, null=True)
    intro = models.TextField(verbose_name='краткое описание',
                             blank=True)
    description = RichTextField(blank=True, verbose_name='описание')
    tags = ClusterTaggableManager(through=MlObjectTag, blank=True, verbose_name='ключи поиска')

    # logical block
    # is system normally operating
    is_enabled = models.BooleanField(default=True, verbose_name='включен')
    # is critical for parent system
    is_critical = models.BooleanField(default=False, verbose_name='критически важен')
    # is object periodically diagnosed
    diagnosed = models.BooleanField(default=True, verbose_name='осмотрен')
    # have normal maintenance
    have_maintenance = models.BooleanField(default=True, verbose_name='обслужен')
    # object have cll-down to it's work
    call_down = models.BooleanField(default=False, verbose_name='есть замечания')
    # system working, but should be repaired
    have_to_be_repaired = models.BooleanField(default=False, verbose_name='требует ремонта')
    # if critical and critically broken, then parent system broken too
    is_critically_broken = models.BooleanField(default=False, verbose_name='сломан')
    # automatic fields
    broken_parts_count = models.IntegerField(default=0, verbose_name='некритичных повреждений')
    critically_broken_parts_count = models.IntegerField(default=0, verbose_name='критичных повреждений')

    # search block
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('description'),
    ]

    # control panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('is_enabled'),
            FieldPanel('is_critical'),
            FieldPanel('diagnosed'),
            FieldPanel('have_maintenance'),
            FieldPanel('call_down'),
            FieldPanel('have_to_be_repaired'),
            FieldPanel('is_critically_broken'),

        ], heading="Состояние объекта",
            classname="collapsible collapsed"),
        FieldPanel('tags'),
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License')
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('buy_date'),
        FieldPanel('broken_parts_count'),
        FieldPanel('critically_broken_parts_count'),
    ]

    class Meta:
        verbose_name = "объект"
        verbose_name_plural = "объекты"
