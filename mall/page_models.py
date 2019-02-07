# Wagtail models (inherited  from page)

# django core modules
from django.db import models

# Wagtail modules
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel,\
    MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
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
    # ToDo: Add tags

    # logical block
    # is system normally operating
    is_enabled = models.BooleanField(default=True, verbose_name='группа включена')
    # is critical for parent system
    is_critical = models.BooleanField(default=True, verbose_name='группа критически важна')
    # is object periodically diagnosed
    diagnosed = models.BooleanField(default=True, verbose_name='группа осмотрена')
    # have normal maintenance
    have_maintenance = models.BooleanField(default=True, verbose_name='группа обслужена')
    # object have cll-down to it's work
    call_down = models.BooleanField(default=False, verbose_name='есть замечания')
    # system working, but should be repaired
    have_to_be_repaired = models.BooleanField(default=False, verbose_name='требует ремонта')
    # if critical and critically broken, then parent system broken too
    is_critically_broken = models.BooleanField(default=False, verbose_name='группа сломана')
    broken_if_all_elements_broken = models.BooleanField(default=False,
                                                        verbose_name='группа сломана если все элементы сломаны')
    # automatic fields
    sub_elements = models.IntegerField(default=0, verbose_name='составные части')
    broken_parts_count = models.IntegerField(default=0, verbose_name='некритичных повреждений')
    critically_broken_parts_count = models.IntegerField(default=0, verbose_name='критичных повреждений')

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
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('is_enabled'),
                FieldPanel('is_critical'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('diagnosed'),
                FieldPanel('have_maintenance'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('call_down'),
                FieldPanel('have_to_be_repaired'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('is_critically_broken', classname="col6"),
                FieldPanel('sub_elements', classname="col6"),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('broken_parts_count'),
                FieldPanel('critically_broken_parts_count'),
            ], classname=None),
        ], heading="Состояние объекта",
            classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('broken_if_all_elements_broken'),
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
    sub_elements = models.IntegerField(default=0, verbose_name='составные части')
    broken_parts_count = models.IntegerField(default=0, verbose_name='некритичных повреждений')
    critically_broken_parts_count = models.IntegerField(default=0, verbose_name='критичных повреждений')

    # search block
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('description'),
    ]

    # logical block
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    # control panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('is_enabled'),
                FieldPanel('is_critical'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('diagnosed'),
                FieldPanel('have_maintenance'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('call_down'),
                FieldPanel('have_to_be_repaired'),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('is_critically_broken', classname="col6"),
                FieldPanel('sub_elements', classname="col6"),
            ], classname=None),
            FieldRowPanel([
                FieldPanel('broken_parts_count'),
                FieldPanel('critically_broken_parts_count'),
            ], classname=None),
        ], heading="Состояние объекта",
            classname="collapsible collapsed"),
        FieldPanel('tags'),
        FieldPanel('intro', classname="full"),
        MultiFieldPanel([
            FieldPanel('description', classname=None),
        ], heading="Описание",
            classname="full collapsible collapsed"),
        MultiFieldPanel([
            InlinePanel('gallery_images', label="Фото объекта"),
        ], heading="Приложенные фото", classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License')
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('buy_date'),

    ]

    class Meta:
        verbose_name = "объект"
        verbose_name_plural = "объекты"


class MlObjectGalleryImage(Orderable):
    page = ParentalKey(MlObjectPage, on_delete=models.CASCADE,
                       related_name='gallery_images',)
    # noinspection PyUnresolvedReferences
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE,
                              related_name='+',
                              verbose_name="фото")
    caption = models.TextField(blank=True,
                               verbose_name="Описание")

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]

