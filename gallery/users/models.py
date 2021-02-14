from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
import os

from gallery.users.storage import OverwriteStorage


def image_path(instance, filename: str):
    """
    Path to where images are stored.

    :param instance: the newly created instance.
    :param filename: the name of the file during upload.
    """
    _, ext = os.path.splitext(filename)
    return "images/{}{}".format(slugify(instance.name), ext)


class User(AbstractUser):
    """Default user for Gallery."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Gallery(TimeStampedModel):
    """Simple gallery database class"""

    image = models.ImageField(upload_to=image_path, storage=OverwriteStorage())
    visible = models.BooleanField(default=False)
    name = models.CharField(unique=True, max_length=127)
    caption = models.TextField(max_length=511)

    FIXED_LENGTH = 128

    @property
    def processed(self):
        return self.visible
