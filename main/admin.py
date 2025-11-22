from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    PrintOrder,
    CallRequest,
    Service,
    SocialLink,
    ContactInfo,
    FAQ,
    HeroImage,
    Stat,
    MarketplaceLink,
    ProjectsBlock,
    OrderFile,
)

class OrderFileInline(admin.TabularInline):
    """Inline для отображения всех файлов заявки"""
    model = OrderFile
    extra = 0
    readonly_fields = ['file', 'created_at', 'get_file_preview']
    fields = ['get_file_preview', 'file', 'created_at']
    can_delete = False
    
    def get_file_preview(self, obj):
        if obj and obj.file:
            file_url = obj.file.url
            file_name = obj.file.name.split('/')[-1]
            # Определяем тип файла для превью
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                return format_html(
                    '<a href="{}" target="_blank"><img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 4px;" /></a>',
                    file_url, file_url
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank">{}</a>',
                    file_url, file_name
                )
        return 'Нет файла'
    get_file_preview.short_description = 'Превью'

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'service_type', 'get_files_count', 'created_at', 'is_processed']
    list_filter = ['created_at', 'is_processed', 'service_type']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at', 'get_all_files']
    list_editable = ['is_processed']
    inlines = [OrderFileInline]
    
    def get_files_count(self, obj):
        """Показывает количество прикрепленных файлов"""
        count = obj.files.count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{} файл(ов)</span>', count)
        return 'Нет файлов'
    get_files_count.short_description = 'Файлы'
    
    def get_all_files(self, obj):
        """Показывает все файлы заявки"""
        files = obj.files.all()
        if files:
            file_list = []
            for order_file in files:
                file_url = order_file.file.url
                file_name = order_file.file.name.split('/')[-1]
                file_list.append(
                    format_html('<a href="{}" target="_blank">{}</a>', file_url, file_name)
                )
            return format_html('<br>'.join(file_list))
        return 'Нет файлов'
    get_all_files.short_description = 'Все файлы'

@admin.register(CallRequest)
class CallRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at', 'is_processed']
    list_filter = ['created_at', 'is_processed']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at']
    list_editable = ['is_processed']

@admin.register(MarketplaceLink)
class MarketplaceLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'title', 'url', 'is_active', 'order']
    list_editable = ['title', 'url', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    search_fields = ['title', 'url', 'description']
    fields = ['platform', 'title', 'url', 'description', 'is_active', 'order']
    ordering = ['order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'title', 'is_active', 'order', 'get_image_preview']
    list_editable = ['title', 'order', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['title', 'description']
    fields = ['service_type', 'title', 'description', 'image', 'is_active', 'order']
    ordering = ['order']
    
    def save_model(self, request, obj, form, change):
        """Принудительно сохраняем изменения"""
        super().save_model(request, obj, form, change)
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;">', obj.image.url)
        return 'Нет изображения'
    get_image_preview.short_description = 'Превью'

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['platform', 'is_active']
    search_fields = ['url']
    fields = ['platform', 'url', 'is_active', 'order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    fields = ['question', 'answer', 'order', 'is_active']
    ordering = ['order']
    
    def save_model(self, request, obj, form, change):
        """Принудительно сохраняем изменения"""
        super().save_model(request, obj, form, change)
    
    def response_change(self, request, obj):
        """Обработка после изменения"""
        from django.contrib import messages
        messages.success(request, 'FAQ успешно обновлен!')
        return super().response_change(request, obj)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'work_hours', 'owner_name', 'inn']
    fields = ['phone', 'email', 'work_hours', 'owner_name', 'inn']
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если записей нет
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Если нет записей, создаем дефолтную
        if not ContactInfo.objects.exists():
            ContactInfo.objects.create()
        return super().changelist_view(request, extra_context)
    
    def save_model(self, request, obj, form, change):
        """Принудительно сохраняем изменения"""
        super().save_model(request, obj, form, change)
    
    def response_change(self, request, obj):
        """Обработка после изменения"""
        from django.contrib import messages
        messages.success(request, 'Контактная информация успешно обновлена!')
        return super().response_change(request, obj)

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['stat_type', 'number', 'label', 'is_active', 'order']
    list_editable = ['number', 'label', 'is_active', 'order']
    list_filter = ['stat_type', 'is_active']
    search_fields = ['label']
    fields = ['stat_type', 'number', 'label', 'icon_class', 'is_active', 'order']
    ordering = ['order']

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'get_image_preview']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'alt_text']
    fields = ['title', 'image', 'alt_text', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если записей нет
        return not HeroImage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление единственной записи
        if HeroImage.objects.count() <= 1:
            return False
        return True
    
    def changelist_view(self, request, extra_context=None):
        # Если нет записей, создаем дефолтную
        if not HeroImage.objects.exists():
            HeroImage.objects.create()
        return super().changelist_view(request, extra_context)
    
    def save_model(self, request, obj, form, change):
        """Принудительно сохраняем изменения"""
        super().save_model(request, obj, form, change)
    
    def response_change(self, request, obj):
        """Обработка после изменения"""
        from django.contrib import messages
        messages.success(request, 'Изображение первого блока успешно обновлено!')
        return super().response_change(request, obj)
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 100px; border-radius: 8px;">', obj.image.url)
        return 'Нет изображения'
    get_image_preview.short_description = 'Превью'


@admin.register(ProjectsBlock)
class ProjectsBlockAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'updated_at']
    SCREEN_LABELS = {
        'main_screenshot': 'Скриншот 1',
        'left_screenshot': 'Скриншот 2',
        'right_screenshot': 'Скриншот 3',
        'main_url': 'Ссылка для скриншота 1',
        'left_url': 'Ссылка для скриншота 2',
        'right_url': 'Ссылка для скриншота 3',
    }
    SCREEN_HELP_TEXTS = {
        'main_screenshot': 'Изображение, отображающееся в большом окне',
        'left_screenshot': 'Изображение в первом малом окне справа',
        'right_screenshot': 'Изображение во втором малом окне справа',
        'main_url': 'Ссылка для перехода при клике по скриншоту 1',
        'left_url': 'Ссылка для перехода при клике по скриншоту 2',
        'right_url': 'Ссылка для перехода при клике по скриншоту 3',
    }
    fieldsets = (
        ('Тексты блока', {
            'fields': ('intro_text', 'marketplace_text', 'social_banner_text')
        }),
        ('Скриншот 1', {
            'fields': ('main_screenshot', 'main_preview', 'main_url'),
            'description': 'Изображение и ссылка, которые отображаются в большом окне'
        }),
        ('Скриншот 2', {
            'fields': ('left_screenshot', 'left_preview', 'left_url'),
            'description': 'Первое из малых окон справа'
        }),
        ('Скриншот 3', {
            'fields': ('right_screenshot', 'right_preview', 'right_url'),
            'description': 'Второе из малых окон справа'
        }),
        ('Статус', {
            'fields': ('is_active', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['main_preview', 'left_preview', 'right_preview', 'updated_at']

    def has_add_permission(self, request):
        return not ProjectsBlock.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if not ProjectsBlock.objects.exists():
            ProjectsBlock.objects.create()
        return super().changelist_view(request, extra_context)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.SCREEN_LABELS:
            formfield.label = self.SCREEN_LABELS[db_field.name]
        if db_field.name in self.SCREEN_HELP_TEXTS:
            formfield.help_text = self.SCREEN_HELP_TEXTS[db_field.name]
        return formfield

    def main_preview(self, obj):
        if obj.main_screenshot:
            return format_html(
                '<img src="{}" style="max-width: 220px; border-radius: 12px;" />',
                obj.main_screenshot.url
            )
        return 'Нет изображения'
    main_preview.short_description = 'Скриншот 1 — превью'

    def left_preview(self, obj):
        if obj.left_screenshot:
            return format_html(
                '<img src="{}" style="max-width: 220px; border-radius: 12px;" />',
                obj.left_screenshot.url
            )
        return 'Нет изображения'
    left_preview.short_description = 'Скриншот 2 — превью'

    def right_preview(self, obj):
        if obj.right_screenshot:
            return format_html(
                '<img src="{}" style="max-width: 220px; border-radius: 12px;" />',
                obj.right_screenshot.url
            )
        return 'Нет изображения'
    right_preview.short_description = 'Скриншот 3 — превью'

