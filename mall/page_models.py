# Wagtail models (inherited  from page)

# django core modules
from django.db import models

# Wagtail modules
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel,\
    MultiFieldPanel, FieldRowPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

# other modules
from datetime import datetime
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtailautocomplete.edit_handlers import AutocompletePanel


# TODO: Make frontend Mall object list
class MlObjectIndexPage(Page):
    intro = models.TextField(verbose_name='краткое описание',
                             blank=True)
    # ToDo: rewrite categories to "orderable" model
    category = models.ForeignKey('mall.MlCategory', on_delete=models.SET_NULL, null=True)
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
        # Default field SnippestChooserPanel is changed to third party AutocompletePanel
        # SnippetChooserPanel('category'),
        AutocompletePanel('category', page_type='mall.MlCategory'),
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

    subpage_types = ['MlObjectPage', 'MlObjectIndexPage']


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


# TODO: Make frontend # List of tags
class MlObjectTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):

        # Filter by tag
        tag = request.GET.get('tag')
        ml_objects = MlObjectPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['ml_objects'] = ml_objects
        return context

    class Meta:
        verbose_name = "ключи поиска"
        verbose_name_plural = "ключи поиска"

# TODO: Make frontend
class MlObjDisposerList(Page):
    pass

    def __str__(self):
        return self.title

    # overriding default get_context to include only live objects, ordered by title
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # can be ordered by published date: order_by('-first_published_at')
        ml_disposer_list = self.get_children().live().order_by('title')
        context['ml_disposer_list'] = ml_disposer_list
        return context

    class Meta:
        verbose_name = "спиок распорядителей"
        verbose_name_plural = "списки распорядителей"

    subpage_types = ['mall.MlObjDisposer', 'mall.MlObjDisposerList']





# TODO: Make frontend # Mall object disposer (for example owner of the shop, which rent the room)
class MlObjDisposer(Page):
    description = RichTextField(blank=True, verbose_name="описание")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('description', classname=None),
        ], heading="Описание",
            classname="full collapsible collapsed"),
        MultiFieldPanel([
            InlinePanel('disposer_docs', label="Приложение"),
        ], heading="Приложенные документы", classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License')]

    def __str__(self):
        return self.title

    class Meta:
        # verbose_name = "object disposer"
        verbose_name = "распорядитель объекта"
        # verbose_name_plural = "object disposers"
        verbose_name_plural = "распорядители объектов"

    parent_page_types = ['mall.MlObjDisposerList']


# TODO: Make frontend # Mall object
class MlObjectPage(Page):
    disposer_id = models.ForeignKey('wagtailcore.Page',
                                    null=True,
                                    blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='+',
                                    verbose_name="распорядитель объекта")
    start_date = models.DateField("начало", blank=True, null=True)
    status_ok = models.BooleanField("параметры в норме", default=True)
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

    # overrride save metod
    def save(self, *args, **kwargs):
        is_crit = self.is_critical
        crit = self.is_critically_broken

        """

        a = self.get_parent(update=True)
        a.specific.is_critically_broken = crit

       
        if crit and is_crit:
            ancestors = reversed(self.get_ancestors())
            for ancestor in ancestors:
                if ancestor.title != "root":
                    with ancestor.specific.is_critically_broken as crit_brok:

                        if crit_brok:
                            is_crit = ancestor.specific.is_critical
                            continue
                        alarm = True

                        with ancestor.specific.broken_if_all_elements_broken as brok:
                            if brok:
                                childr = ancestors.get_children().live()
                                for child in childr:
                                    if (child.specific.is_critically_broken == False) and \
                                            (child.specific.is_critical == True):
                                        alarm = False
                        if is_crit:
                            ancestor.specific.is_critically_broken = alarm
                            is_crit = ancestor.specific.is_critical
        """
        #TODO: change tags claster (self.tags.add('auto_alarm',"events"))
        super(MlObjectPage, self).save()

    # control panels
    content_panels = Page.content_panels + [

        # Default field PageChooserPanel is changed to third party AutocompletePanel
        # PageChooserPanel('disposer_id', 'mall.MlObjDisposer'),
        MultiFieldPanel([
            AutocompletePanel('disposer_id', page_type='mall.MlObjDisposer'),
            FieldRowPanel([
                FieldPanel('start_date'),
                FieldPanel('status_ok'),
            ], classname=None),
        ], heading="Кто расроряжается:", classname="collapsible collapsed"),
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
            InlinePanel('ml_obj_docs', label="Приложение"),
        ], heading="Приложенные документы", classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License'),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            InlinePanel('gallery_images', label="Фото объекта"),
        ], heading="Приложенные фото", classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License'),
    ]

    settings_panels = Page.settings_panels + [


    ]

    parent_page_types = ['mall.MlObjectIndexPage']
    #subpage_types = []

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


# attachments for objects
class MlObjectLibrary(Orderable):
    page = ParentalKey(MlObjectPage, on_delete=models.CASCADE,
                       related_name='ml_obj_docs',)
    # noinspection PyUnresolvedReferences
    document = models.ForeignKey('wagtaildocs.Document',
                              on_delete=models.CASCADE,
                              related_name='+',
                              verbose_name="документ")
    caption = models.TextField(blank=True,
                               verbose_name="Описание")

    panels = [
        DocumentChooserPanel('document'),
        FieldPanel('caption')
    ]


# attachments for disposers
class DisposerLibrary(Orderable):
    page = ParentalKey(MlObjDisposer, on_delete=models.CASCADE,
                       related_name='disposer_docs',)
    # noinspection PyUnresolvedReferences
    document = models.ForeignKey('wagtaildocs.Document',
                              on_delete=models.CASCADE,
                              related_name='+',
                              verbose_name="документ")
    caption = models.TextField(blank=True,
                               verbose_name="Описание")

    panels = [
        DocumentChooserPanel('document'),
        FieldPanel('caption')
    ]
