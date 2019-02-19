from wagtail.core.signals import page_published
from mall.models import *
import logging

logger = logging.getLogger(__name__)


def critically_broken(instance_page_specific, parent_page_specific):
    # if critical instance is critically broken > parent is critically broken
    logger.debug(f"updating {parent_page_specific}, parent of {instance_page_specific}")
    if instance_page_specific.is_critically_broken and instance_page_specific.is_critical:
        old_parent_is_critically_broken = parent_page_specific.is_critically_broken
        parent_page_specific.is_critically_broken = True
        logger.debug(f"parent is_critically_broken if instance is_critically_broken. Parent: \
                    {old_parent_is_critically_broken} > {parent_page_specific.is_critically_broken}")
    return parent_page_specific


# MlObjectPage
def ml_object_page_receiver(instance, *args, **kwargs):
    parent_page = instance.get_parent()
    if parent_page.specific_class == MlObjectIndexPage:
        parent_page_specific = parent_page.specific
        instance_page_specific = instance.specific
        # if critical instance is critically broken > parent is critically broken
        parent_page_specific = critically_broken(instance_page_specific, parent_page_specific)

        """
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
        """
        # call Page save() method (instance.save() not work)
        # parent_page_specific.save_revisions()
        parent_page_specific.save_revision().publish()
        # super(Page, parent_page_specific).save()

        # print(Page.objects.get(id=p2.id).specific.is_critical)
        # print(Page.objects.get(id=parent_page_specific.id).specific.is_critical)

    if parent_page.specific_class == MlObjectPage:
        # print("parent is MlObjectPage")
        parent_page_specific = parent_page.specific
        instance_page_specific = instance.specific
        # if critical instance is critically broken > parent is critically broken
        parent_page_specific = critically_broken(instance_page_specific, parent_page_specific)
        # parent_page_specific.save_revisions()
        parent_page_specific.save_revision().publish()
        # super(Page, parent_page_specific).save()


page_published.connect(ml_object_page_receiver, sender=MlObjectPage)


# MlObjectIndexPage
def ml_object_index_page_receiver(instance, *args, **kwargs):
    parent_page = instance.get_parent()
    if parent_page.specific_class == MlObjectPage:
        parent_page_specific = parent_page.specific
        instance_page_specific = instance.specific
        # if critical instance is critically broken > parent is critically broken
        parent_page_specific = critically_broken(instance_page_specific, parent_page_specific)
        # parent_page_specific.save_revisions()
        parent_page_specific.save_revision().publish()
        # super(Page, parent_page_specific).save()

    if parent_page.specific_class == MlObjectIndexPage:
        parent_page_specific = parent_page.specific
        instance_page_specific = instance.specific
        # if critical instance is critically broken > parent is critically broken
        parent_page_specific = critically_broken(instance_page_specific, parent_page_specific)
        # parent_page_specific.save_revisions()
        parent_page_specific.save_revision().publish()
        # super(Page, parent_page_specific).save()


page_published.connect(ml_object_index_page_receiver, sender=MlObjectIndexPage)

