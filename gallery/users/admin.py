from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from gallery.users.forms import UserChangeForm, UserCreationForm, GalleryCreationForm
from gallery.users.models import Gallery

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name", "caption", "image",)
        }),
    )
    list_display = ["name", "processed", "caption", "created", "modified"]
    search_fields = ["name"]
