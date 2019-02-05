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
    intro = models.CharField(max_length=255,
                             verbose_name='краткое описание',
                             blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
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
    intro = models.CharField(max_length=255,
                             verbose_name='краткое описание',
                             blank=True)
    description = RichTextField(blank=True, verbose_name='описание')
    tags = ClusterTaggableManager(through=MlObjectTag, blank=True, verbose_name='ключи поиска')

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('buy_date'),
            FieldPanel('tags'),
        ], heading="Ключи поиска"),
        FieldPanel('intro'),
        FieldPanel('description', classname="full"),
    ]

    class Meta:
        verbose_name = "объект"
        verbose_name_plural = "объекты"
