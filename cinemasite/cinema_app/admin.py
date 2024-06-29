from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Cinema, Category


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['title', 'cat', 'display_image', 'year_production', 'time_create', 'is_active']
    list_display_links = ['title']
    search_fields = ['title', 'cat__name']
    search_help_text = 'Поиск по фильмам и категориям'
    ordering = ['time_create', 'title']
    list_editable = ['is_active']
    list_per_page = 10
    actions = ['set_active', 'set_draft']
    list_filter = ['cat__name', 'is_active']

    fields = ['title', 'descriptions', 'display_image', 'photo', 'year_production', 'cat', 'slug', 'genres']
    readonly_fields = ['slug', 'display_image']
    filter_horizontal = ['genres']

    @admin.display()
    def display_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width=40>')
        return 'Фото отсутствует'

    display_image.short_description = 'Изображение'

    @admin.action(description='Активировать')
    def set_active(self, request, queryset):
        count = queryset.update(is_active=Cinema.Status.ACTIVE)
        self.message_user(request, f'Активировано {count} фильмов')

    @admin.action(description='Деактивировать')
    def set_draft(self, request, queryset):
        count = queryset.update(is_active=Cinema.Status.DRAFT)
        self.message_user(request, f'Деактивировано {count} фильмов', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
