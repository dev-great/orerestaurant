from django.contrib import admin
from django.utils.html import format_html

from .models import (
    MenuItem,
    MenuItemTag, MenuItemImage, Rating, Review
)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'short_description',
                    'availability', 'created_on', 'updated_on']
    list_filter = ['availability']
    search_fields = ['name', 'description']

    def short_description(self, obj):
        max_length = 50
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description

    short_description.short_description = 'Description'


admin.site.register(MenuItem, MenuItemAdmin)


class MenuItemTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on', 'updated_on']
    search_fields = ['name']


admin.site.register(MenuItemTag, MenuItemTagAdmin)


class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ['menu_item_id',
                    'image_display', 'created_on', 'updated_on']
    search_fields = ["menu_item_id", ]

    readonly_fields = ['image_preview',]

    def image_display(self, obj):
        return format_html('<img src="{}" width="110" height="100" />', obj.image.url)

    def image_preview(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    image_display.short_description = 'Primary Image'
    image_preview.short_description = 'Primary Image Preview'


admin.site.register(MenuItemImage, MenuItemImageAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'rating', 'created_on', 'updated_on']
    list_filter = ['rating']
    search_fields = ['user__email', 'menu_item__name']


admin.site.register(Rating, RatingAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'comment', 'created_on', 'updated_on']
    search_fields = ['user__email', 'menu_item__name']


admin.site.register(Review, ReviewAdmin)
