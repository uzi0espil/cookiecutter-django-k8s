from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from gallery.users.models import Gallery
from gallery.users.tasks import resize_images


@receiver(post_save, sender=Gallery)
def resize_image(sender, instance: Gallery, created, **kwargs):
    if instance.image.width != Gallery.FIXED_LENGTH:
        resize_images.apply_async((instance.id,))


@receiver(post_delete, sender=Gallery)
def delete_image(sender, instance: Gallery, **kwargs):
    instance.image.delete(False)
