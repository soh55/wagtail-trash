from django.urls import path
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import IndexView
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from .utils import recycle_bin_for_request
from .models import RecycleBinPage
from .views import recycle_delete


class RecycleButtonHelper(ButtonHelper):
    restore_button_classnames = [
        "button-small",
        "button-secondary",
        "icon",
        "icon-undo",
    ]

    def restore_button(self, obj):
        return {
            "url": "/",
            "label": "Restore",
            "classname": self.finalise_classname(self.restore_button_classnames),
            "title": "Restore",
        }

    def get_buttons_for_obj(
        self, obj, exclude=["edit"], classnames_add=None, classnames_exclude=None
    ):
        buttons = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )

        print(buttons)

        if "restore" not in (exclude or []):
            buttons.append(self.restore_button(obj))

        return buttons


class RecycleBinModelAdmin(ModelAdmin):
    model = Page
    menu_label = "Recycle Bin"
    menu_icon = "bin"
    admin_order_field = "title"

    list_display = ("title", "sub_pages")
    search_fields = ("title",)

    button_helper_class = RecycleButtonHelper

    def sub_pages(self, page):
        return [x.title for x in page.get_descendants()]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        recycle_bin = recycle_bin_for_request(request)

        return recycle_bin.get_children()


modeladmin_register(RecycleBinModelAdmin)


@hooks.register("before_delete_page")
def delete_page(request, page):
    return recycle_delete(request, page)


@hooks.register("construct_page_chooser_queryset")
def exclude_recycle_bin_from_chooser(pages, request):
    pages = pages.not_type(RecycleBinPage)

    return pages


@hooks.register("construct_explorer_page_queryset")
def exclude_recycle_bin_from_explorer(parent_page, pages, request):
    pages = pages.not_type(RecycleBinPage)

    return pages