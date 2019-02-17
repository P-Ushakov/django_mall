from wagtail.core.signals import page_published
from mall.models import *
import logging

logger = logging.getLogger(__name__)

# MlObjectPage
def ml_object_page_receiver(instance,*args, **kwargs):

    parent_page = instance.get_parent()

    if parent_page.specific_class == MlObjectIndexPage:
        logger.debug(f"updating {parent_page}, parent of {instance}")
        parent_page_specific = parent_page.specific
        instance_page_specific = instance.specific

        # if critical instance is critically broken > parent is critically broken
        if instance_page_specific.is_critically_broken and instance_page_specific.is_critical:
            old_parent_is_critically_broken = parent_page_specific.is_critically_broken
            parent_page_specific.is_critically_broken = True
            logger.debug(f"parent is_critically_broken if instance is_critically_broken. Parent: \
                          {old_parent_is_critically_broken} > {parent_page_specific.is_critically_broken}")

        # instance have to be repaired > parent have to be repaired
        if instance_page_specific.have_to_be_repaired:
            old_parent_have_to_be_repaired = parent_page_specific.have_to_be_repaired
            parent_page_specific.have_to_be_repaired = True
            logger.debug(f"parent have_to_be_repaired if instance have_to_be_repaired. Parent: \
                                      {old_parent_have_to_be_repaired} > {parent_page_specific.have_to_be_repaired}")

            # have broken siblings num of N > parent critically broken
            broken_siblings_alowwed = parent_page_specific.broken_if_num_elements_broken
            broken_siblings = 0
            for sibling in instance.get_siblings(inclusive=True):
                broken_siblings += int(sibling.specific.have_to_be_repaired)
            if broken_siblings >= broken_siblings_alowwed:
                parent_page_specific.is_critically_broken = True

        # call Page save() method (instance.save() not work)
        super(Page, parent_page_specific).save()

        # print(Page.objects.get(id=p2.id).specific.is_critical)
        # print(Page.objects.get(id=parent_page_specific.id).specific.is_critical)

    if parent_page.specific_class == MlObjectPage:
        # print("parent is MlObjectPage")
        pass


page_published.connect(ml_object_page_receiver, sender=MlObjectPage)
