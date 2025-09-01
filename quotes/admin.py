from django.contrib import admin
from .models import Source, Quote

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """
    Класс для отображения и фильтрации источников цитат
    """
    list_display = ['name', 'type']
    list_filter = ['type']

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Класс для отображения и фильтрации цитат
    """
    list_display = ['text_short', 'source', 'weight', 'views', 'likes', 'dislikes']
    list_editable = ['weight']
    list_filter = ['source']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'
    

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'weight':
            field.widget.attrs['min'] = 1
            field.widget.attrs['max'] = 10
        return field