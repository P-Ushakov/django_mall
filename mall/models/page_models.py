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

# other tags, that can be used ☀ ⁇ ✅ ⛔ 🌦️ ‼
# AUTOMATIC TAGS                symbol  description  border  influence
TAG_DICT = {
    'status_ok':            ("✔", "статус Ok", "success", 7),  # ✔
    'status_bad':           (chr(9940), "статус Bad", "danger", 25),  # ⛔
    'is_enabled':           ("💡", "включен", "success", 5),  # 💡
    'is_disabled':          ("🔌", "выключен", "dark", 21),  # 🔌
    'diagnosed':            (chr(9874), "осмотрен", "success", 3),  # ⚒
    'have_to_be_diagnosed': (chr(9200), "пришло время осмотра", "info", 15),  # ⏰
    'need_service':         (chr(9997), "пришло время TO", "info", 18),  # ✍
    'have_maintenance':     (chr(9730), "прошел ТО", "success", 2),  # ☂
    'is_critical':          (chr(9889), "критически важен", "success", 4),  # ⚡
    'call_down':            (chr(9785), "есть замечания", "warning", 20),  # ☹
    'have_to_be_repaired':  (chr(9888), "требует ремонта", "warning", 23),  # ⚠
    'is_critically_broken': (chr(9760), "сломан", "danger", 28),  # ☠
}


# TODO: Make frontend Mall object list
class MlObjectIndexPage(Page):
    intro = models.TextField(verbose_name='краткое описание',
                             blank=True)
    # ToDo: rewrite categories to "orderable" model
    category = models.ForeignKey('mall.MlCategory',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='+')
    # logical block
    # is system normally operating
    # TODO rewrite it to integer and change bages to represent cached data
    # TODO write metod to populate cashed data on descendants update
    status_ok = models.IntegerField(default=0, verbose_name='статус OK')
    status_bad = models.IntegerField(default=0, verbose_name='статус Bad')
    is_enabled = models.IntegerField(default=0, verbose_name='включено')
    is_disabled = models.IntegerField(default=0, verbose_name='выключено')
    # is object periodically diagnosed
    diagnosed = models.IntegerField(default=0, verbose_name='произведен осмотр')
    have_to_be_diagnosed = models.IntegerField(default=0, verbose_name='требует осмотра')
    # have normal maintenance
    have_maintenance = models.IntegerField(default=0, verbose_name='пройдено ТО')
    need_service = models.IntegerField(default=0, verbose_name='требует ТО')
    # object have call-down to it's work
    call_down = models.IntegerField(default=0, verbose_name='есть замечания')
    # system working, but should be repaired
    have_to_be_repaired = models.IntegerField(default=0, verbose_name='требует ремонта')

    # is critical for parent system
    is_critical = models.IntegerField(default=0, verbose_name='критически важный элемент')
    # if critical and critically broken, then parent system broken too
    is_critically_broken = models.IntegerField(default=0, verbose_name='сломано')
    # settings fields

    # group is visible for tags. If False - group close local scope of tags
    is_visible_for_tags = models.BooleanField(default=True, verbose_name="группа видна для дочерних меток")
    partial_cache_reset = models.BooleanField(default=False, verbose_name="частичный сброс кэшированных данных")
    full_cache_reset = models.BooleanField(default=False, verbose_name="полный сброс кэшированных данных")

    # overriding default get_context to include only live objects, ordered by title
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # can be ordered by published date: order_by('-first_published_at')
        ml_objects = self.get_children().live().order_by('title')
        context['ml_objects'] = ml_objects
        return context

    # colored borders for objects
    def ml_list_alert_color(self):
        alert = "border-success"
        if self.need_service or self.have_to_be_diagnosed:
            alert = "alert-info"
        elif self.is_disabled:
            alert = "alert-secondary"
        elif self.have_to_be_repaired or self.call_down or self.status_bad:
            alert = "alert-warning"
        elif self.is_critically_broken:
            alert = "alert-danger"

        return alert



    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        # Default field SnippestChooserPanel is changed to third party AutocompletePanel
        # SnippetChooserPanel('category'),
        # PageChooserPanel('category'),
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
            ], classname=None),
        ], heading="Состояние объекта",
            classname="collapsible collapsed"),
        MultiFieldPanel([], heading='© Pavel Ushakov, BSD License'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('is_visible_for_tags'),
        FieldPanel('partial_cache_reset'),
        FieldPanel('full_cache_reset'),
    ]

    class Meta:
        verbose_name = "список объектов"
        verbose_name_plural = "списоки объектов"

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


# Mall object tag
class MlObjectAutoTag(TaggedItemBase):
    content_object = ParentalKey(
        'MlObjectPage',
        related_name='ml_obj_auto_tags',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "состояние"
        verbose_name_plural = "состояние"


# TODO: Make frontend # List of tags
class MlObjectTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):

        # Filter by tag
        tag = request.GET.get('tag')
        id = int(request.GET.get('id'))
        # Вот уж намудрили с фильтрами :(
        # ml_object_tags = MlObjectPage.objects.filter(models.Q(auto_tags__name=tag) | models.Q(tags__name=tag))
        ml_object = Page.objects.get(id=id)

        # parent_ml_object = ml_object.get_parent()
        descendants_ml_objects = MlObjectPage.objects.descendant_of(ml_object, inclusive=True).live()
        ml_object_tags = descendants_ml_objects.filter(auto_tags__name=tag)

        # manual tags: lift up on the tree root before finding "is_visible_for_tags : False
        if not ml_object_tags:
            ancestors_ml_object_group = \
                reversed(MlObjectIndexPage.objects.ancestor_of(ml_object))
            for ancestor in ancestors_ml_object_group:
                if ancestor.specific.is_visible_for_tags:
                    ml_object = ancestor
            ml_object_parent = ml_object.get_parent()
            if ml_object_parent.specific_class == MlObjectPage:
                ml_object = ml_object_parent
            descendants_ml_objects = MlObjectPage.objects.descendant_of(ml_object, inclusive=True).live()
            ml_object_tags = descendants_ml_objects.filter(tags__name=tag)
        """
        ml_object_tags = MlObjectPage.objects.filter(auto_tags__name=tag)
        if not ml_object_tags:
            ml_object_tags = MlObjectPage.objects.filter(tags__name=tag)
        """
        # Update template context
        context = super().get_context(request)
        context['ml_object_tags'] = ml_object_tags
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
    install_date = models.DateField("дата установки", blank=True, null=True)
    status_ok = models.BooleanField("параметры в норме", default=True)
    intro = models.TextField(verbose_name='краткое описание',
                             blank=True)
    description = RichTextField(blank=True, verbose_name='описание')
    tags = ClusterTaggableManager(through=MlObjectTag, blank=True, verbose_name='ключи поиска')
    auto_tags = ClusterTaggableManager(through=MlObjectAutoTag,
                                       blank=True,
                                       verbose_name='состояние',
                                       related_name='ml_obj_auto_tags',)

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

    # search block
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('description'),
    ]

    # logical block
    # getters and setters
    @property
    def status_bad(self):
        return not self.status_ok

    @status_bad.setter
    def status_bad(self, value):
        self.status_ok = not value

    @property
    def is_disabled(self):
        return not self.is_enabled

    @is_disabled.setter
    def is_disabled(self, value):
        self.is_enabled = not value

    @property
    def have_to_be_diagnosed(self):
        return not self.diagnosed

    @have_to_be_diagnosed.setter
    def have_to_be_diagnosed(self, value):
        self.diagnosed = not value

    @property
    def need_service(self):
        return not self.have_maintenance

    @need_service.setter
    def need_service(self, value):
        self.have_maintenance = not value

    # FixMe
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    # colored borders for objects
    def ml_obj_border(self):
        tags = self.auto_tags.all()
        border = "success"
        influence = 0
        for tag in tags:
            for key in TAG_DICT:
                if TAG_DICT[key][0] == tag.name and influence < TAG_DICT[key][3]:
                    influence = TAG_DICT[key][3]
                    border = TAG_DICT[key][2]
        return border

    # override save method
    def save(self, *args, **kwargs):

        if self.is_critically_broken:
            self.have_to_be_repaired = True

        if self.have_to_be_repaired:
            self.status_ok = False

        self.auto_tags.clear()

        status_args = ('status_ok', 'status_bad', 'is_enabled', 'is_disabled', 'diagnosed',
                       'have_to_be_diagnosed', 'have_maintenance', 'need_service', 'is_critical',
                       'call_down', 'have_to_be_repaired', 'is_critically_broken')
        for status in status_args:
            if getattr(self, status):
                self.auto_tags.add(TAG_DICT[status][0])

        """
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
                FieldPanel('install_date'),
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
            ], classname=None),
        ], heading="Состояние объекта",
            classname="collapsible collapsed"),
        FieldPanel('tags'),
        FieldPanel('auto_tags'),
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
