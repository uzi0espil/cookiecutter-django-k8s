from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django import forms
import shutil
import os

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_message = admin_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class GalleryCreationForm(forms.ModelForm):

    # def clean_image(self):
    #     value = self.cleaned_data.get("image")
    #     filename, ext = os.path.splitext(value.name)
    #     new_name = "/app_temp/{}{}".format(slugify(self.data.get('name')), ext)
    #
    #     os.rename(value.temporary_file_path(), new_name)
    #     value.file.name = new_name
    #     return None

    def save(self, commit=True):
        print(self.cleaned_data['image'])
        filename, ext = os.path.splitext(self.cleaned_data['image'].name)
        new_name = "/app_temp/{}{}".format(slugify(self.cleaned_data['name']), ext)

        os.rename(self.cleaned_data['image'].temporary_file_path(), new_name)
        self.cleaned_data['image'].file.name = new_name

        self.cleaned_data['image'] = None
        return super(GalleryCreationForm, self).save(commit=commit)
