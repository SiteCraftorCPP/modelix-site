from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import PrintOrder, CallRequest, Service, SocialLink, ContactInfo, FAQ, HeroImage, Stat, MarketplaceLink, ProjectsBlock

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'service_type', 'created_at', 'is_processed']
    list_filter = ['created_at', 'is_processed', 'service_type']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']
    list_editable = ['is_processed']

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
    list_display = ['get_main_preview', 'get_left_preview', 'get_right_preview', 'is_active', 'updated_at']
    
    fieldsets = (
        ('Тексты', {
            'fields': ('intro_text', 'social_banner_text', 'marketplace_text')
        }),
        ('Главное окно (центр)', {
            'fields': ('main_screenshot', 'main_url'),
            'description': 'Скриншот и ссылка для главного (центрального) окна'
        }),
        ('Левое окно', {
            'fields': ('left_screenshot', 'left_url'),
            'description': 'Скриншот и ссылка для левого окна (при клике меняет главное)'
        }),
        ('Правое окно', {
            'fields': ('right_screenshot', 'right_url'),
            'description': 'Скриншот и ссылка для правого окна (при клике меняет главное)'
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        return not ProjectsBlock.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        if not ProjectsBlock.objects.exists():
            ProjectsBlock.get_instance()
        return super().changelist_view(request, extra_context)
    
    def get_main_preview(self, obj):
        if obj.main_screenshot:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 90px; border-radius: 8px;">', obj.main_screenshot.url)
        return 'Нет скриншота'
    get_main_preview.short_description = 'Главный'
    
    def get_left_preview(self, obj):
        if obj.left_screenshot:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 60px; border-radius: 8px;">', obj.left_screenshot.url)
        return '—'
    get_left_preview.short_description = 'Левый'
    
    def get_right_preview(self, obj):
        if obj.right_screenshot:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 60px; border-radius: 8px;">', obj.right_screenshot.url)
        return '—'
    get_right_preview.short_description = 'Правый'
