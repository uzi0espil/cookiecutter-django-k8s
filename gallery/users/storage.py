from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import glob


class OverwriteStorage(FileSystemStorage):
    """
    FileSystemStorage class that overrides the default setting by overriding the stored files.
    """
    def get_available_name(self, name, max_length=None):
        filename, extension = os.path.splitext(name)
        try:
            # check if file exists regardless of ext.
            for old_file in glob.glob(os.path.join(settings.MEDIA_ROOT, filename + ".*")):
                os.remove(old_file)
        except OSError:
            pass
        return name
