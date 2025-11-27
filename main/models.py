from django.db import models

class PrintOrder(models.Model):
    """Модель для заявок на печать"""
    SERVICE_TYPE_CHOICES = [
        ('other', 'Другое'),
        ('complex', 'Комплекс услуг'),
        ('3d_modeling', '3D моделирование'),
        ('3d_printing', '3D печать'),
        ('3d_scanning', '3D сканирование'),
        ('reverse_engineering', 'Реверс-инжиниринг'),
        ('engineering', 'Инжиниринг'),
        ('post_processing', 'Постобработка'),
    ]
    
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    service_type = models.CharField('Тип услуги', max_length=30, choices=SERVICE_TYPE_CHOICES, default='other', blank=True)
    message = models.TextField('Сообщение')
    file = models.FileField('Файл модели', upload_to='orders/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        verbose_name = 'Заявка на печать'
        verbose_name_plural = 'Заявки на печать'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Заявка от {self.name} - {self.created_at.strftime("%d.%m.%Y %H:%M")}'

    def get_all_files(self):
        """Возвращает все файлы заявки (из OrderFile)"""
        return self.files.all()
    
    def get_all_file_paths(self):
        """Возвращает список путей ко всем файлам заявки"""
        return [order_file.file.path for order_file in self.files.all()]
    
    def get_all_file_urls(self):
        """Возвращает список URL всех файлов заявки"""
        return [order_file.file.url for order_file in self.files.all()]

class OrderFile(models.Model):
    """Модель для хранения файлов заявки"""
    order = models.ForeignKey(PrintOrder, on_delete=models.CASCADE, related_name='files', verbose_name='Заявка')
    file = models.FileField('Файл', upload_to='orders/')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Файл заявки'
        verbose_name_plural = 'Файлы заявок'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.file.name} - {self.order.name}'

class MarketplaceLink(models.Model):
    """Модель для ссылок на маркетплейсы и соц сети"""
    PLATFORM_CHOICES = [
        ('vk_group', 'Группа ВКонтакте'),
        ('telegram', 'Telegram'),
        ('youtube', 'YouTube'),
        ('ozon', 'Озон'),
        ('avito', 'Авито'),
    ]
    
    ICON_MAP = {
        'vk_group': 'fab fa-vk',
        'telegram': 'fab fa-telegram-plane',
        'youtube': 'fab fa-youtube',
        'ozon': 'fas fa-shopping-bag',
        'avito': 'fas fa-shopping-cart',
    }
    
    COLOR_MAP = {
        'vk_group': '#4680c2',
        'telegram': '#0088cc',
        'youtube': '#ff0000',
        'ozon': '#005BFF',
        'avito': '#FF6C37',
    }
    
    platform = models.CharField('Платформа', max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField('Ссылка', max_length=200)
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, max_length=200)
    is_active = models.BooleanField('Активна', default=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Ссылка на маркетплейс/соц сеть'
        verbose_name_plural = 'Маркетплейсы и соц сети'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.get_platform_display()} - {self.title}'
    
    def get_icon_class(self):
        """Возвращает CSS класс для иконки"""
        return self.ICON_MAP.get(self.platform, 'fas fa-link')
    
    def get_platform_color(self):
        """Возвращает цвет платформы"""
        return self.COLOR_MAP.get(self.platform, '#191970')

class FAQ(models.Model):
    """Модель для часто задаваемых вопросов"""
    question = models.CharField('Вопрос', max_length=200)
    answer = models.TextField('Ответ')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ['order']
    
    def __str__(self):
        return self.question

class CallRequest(models.Model):
    """Модель для заявок на звонок"""
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        verbose_name = 'Заявка на звонок'
        verbose_name_plural = 'Заявки на звонок'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Звонок {self.name} - {self.created_at.strftime("%d.%m.%Y %H:%M")}'

class Service(models.Model):
    """Модель для управления услугами (Наши 3D-возможности)"""
    SERVICE_CHOICES = [
        ('3d_modeling', '3D моделирование'),
        ('3d_printing', '3D печать'),
        ('3d_scanning', '3D сканирование'),
        ('reverse_engineering', 'Реверс-инжиниринг'),
        ('engineering', 'Инжиниринг'),
        ('post_processing', 'Постобработка'),
    ]
    
    service_type = models.CharField('Тип услуги', max_length=20, choices=SERVICE_CHOICES, unique=True)
    title = models.CharField('Название услуги', max_length=100)
    description = models.TextField('Описание услуги')
    image = models.ImageField('Изображение', upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги (Наши 3D-возможности)'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.get_service_type_display()} - {self.title}'

class SocialLink(models.Model):
    """Модель для управления социальными ссылками"""
    SOCIAL_CHOICES = [
        ('telegram', 'Telegram'),
        ('vk', 'VKontakte'),
        ('youtube', 'YouTube'),
    ]
    
    platform = models.CharField('Социальная сеть', max_length=20, choices=SOCIAL_CHOICES, unique=True)
    url = models.URLField('Ссылка', max_length=200)
    is_active = models.BooleanField('Активна', default=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Социальная ссылка'
        verbose_name_plural = 'Социальные ссылки'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.get_platform_display()} - {self.url}'
    
    def get_icon_class(self):
        """Возвращает CSS класс для иконки"""
        icon_map = {
            'telegram': 'fab fa-telegram-plane',
            'vk': 'fab fa-vk',
            'youtube': 'fab fa-youtube',
        }
        return icon_map.get(self.platform, 'fas fa-link')

class ContactInfo(models.Model):
    """Модель для управления контактной информацией"""
    phone = models.CharField('Телефон', max_length=20, default='+7 (929) 178-20-00')
    email = models.EmailField('Email', default='modelix.stl@gmail.com')
    work_hours = models.CharField('Часы работы', max_length=50, default='ПН-ПТ 10:00-20:00')
    owner_name = models.CharField('ФИО владельца', max_length=100, default='ИП Худолей Илья Константинович')
    inn = models.CharField('ИНН', max_length=20, default='780618190040')
    
    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'
    
    def __str__(self):
        return 'Контактная информация'
    
    def save(self, *args, **kwargs):
        # Простое сохранение без сложной логики
        return super().save(*args, **kwargs)

class Stat(models.Model):
    """Модель для управления статистикой"""
    STAT_CHOICES = [
        ('experience', 'Опыт работы'),
        ('orders', 'Выполненные заказы'),
        ('technologies', 'Технологии печати'),
    ]
    
    ICON_CHOICES = [
        ('fa-calendar-alt', 'Календарь'),
        ('fa-check-circle', 'Галочка'),
        ('fa-cube', 'Куб'),
    ]
    
    stat_type = models.CharField('Тип статистики', max_length=20, choices=STAT_CHOICES, unique=True)
    number = models.CharField('Число', max_length=20, default='3+')
    label = models.CharField('Подпись', max_length=100)
    icon_class = models.CharField('CSS класс иконки', max_length=50, choices=ICON_CHOICES, default='fa-calendar-alt')
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.get_stat_type_display()} - {self.number} {self.label}'

class HeroImage(models.Model):
    """Модель для управления изображением в hero блоке"""
    title = models.CharField('Название', max_length=100, default='Главное изображение')
    image = models.ImageField('Изображение', upload_to='hero/', default='hero/hero_block1.png')
    alt_text = models.CharField('Альтернативный текст', max_length=200, default='3D принтер')
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Изображение первого блока'
        verbose_name_plural = 'Изображения первого блока'
    
    def __str__(self):
        return f'{self.title} - {self.created_at.strftime("%d.%m.%Y")}'
    
    def save(self, *args, **kwargs):
        # Простое сохранение без очистки кэша
        return super().save(*args, **kwargs)
    
    @property
    def image_url_with_cache_bust(self):
        """Возвращает URL изображения с параметром cache-busting"""
        if self.image:
            import time
            return f"{self.image.url}?v={int(time.time())}"
        return ""

class WorksBlock(models.Model):
    """Модель для управления блоком 'Наши работы' (DEPRECATED - используйте ProjectsBlock)"""
    youtube_screenshot = models.ImageField('Скриншот YouTube', upload_to='works/', blank=True, null=True, help_text='Скриншот с видосами из YouTube')
    youtube_url = models.URLField('Ссылка на YouTube', max_length=200, blank=True, default='', help_text='Ссылка на YouTube канал или плейлист')
    bottom_text = models.TextField('Текст внизу', default='Ознакомьтесь с нашими работами в соц сетях и на маркетплейсах', max_length=200)
    is_active = models.BooleanField('Активен', default=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Блок "Наши работы" (старый)'
        verbose_name_plural = 'Блок "Наши работы" (старый)'
    
    def __str__(self):
        return 'Блок "Наши работы" (старый)'
    
    def save(self, *args, **kwargs):
        # Разрешаем только одну запись
        self.pk = 1
        super(WorksBlock, self).save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Получить единственный экземпляр или создать новый"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    @property
    def youtube_screenshot_url(self):
        """Возвращает URL скриншота с cache-busting"""
        if self.youtube_screenshot:
            import time
            return f"{self.youtube_screenshot.url}?v={int(time.time())}"
        return ""

class ProjectsBlock(models.Model):
    """Модель для управления блоком 'НАШИ ПРОЕКТЫ'"""
    # Тексты
    intro_text = models.TextField('Текст о соцсетях', default='С примерами проектов и тем, как мы их реализуем, можно ознакомиться в наших соцсетях.', max_length=200)
    marketplace_text = models.TextField('Текст о продукции', default='Также, помимо индивидуальных проектов, мы выпускаем готовую продукцию; оценить её качество и прочитать отзывы можно на наших онлайн-витринах.', max_length=300)
    social_banner_text = models.TextField('Текст плашки соцсетей', default='Вы можете смотреть нас в социальных сетях', max_length=150)
    
    # Главное окно (центр)
    main_screenshot = models.ImageField('Главный скриншот', upload_to='projects/', blank=True, null=True, help_text='Скриншот, который отображается по умолчанию')
    main_url = models.URLField('Главная ссылка', max_length=200, blank=True, default='', help_text='Ссылка при клике на главный скриншот')
    
    # Левое окно
    left_screenshot = models.ImageField('Левый скриншот', upload_to='projects/', blank=True, null=True, help_text='Скриншот в левом окне')
    left_url = models.URLField('Левая ссылка', max_length=200, blank=True, default='', help_text='Ссылка при клике на левый скриншот')
    
    # Правое окно
    right_screenshot = models.ImageField('Правый скриншот', upload_to='projects/', blank=True, null=True, help_text='Скриншот в правом окне')
    right_url = models.URLField('Правая ссылка', max_length=200, blank=True, default='', help_text='Ссылка при клике на правый скриншот')
    
    is_active = models.BooleanField('Активен', default=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Блок "НАШИ ПРОЕКТЫ"'
        verbose_name_plural = 'Блок "НАШИ ПРОЕКТЫ"'
    
    def __str__(self):
        return 'Блок "НАШИ ПРОЕКТЫ"'
    
    def save(self, *args, **kwargs):
        # Разрешаем только одну запись
        self.pk = 1
        super(ProjectsBlock, self).save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Получить единственный экземпляр или создать новый"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    @property
    def main_screenshot_url(self):
        """Возвращает URL главного скриншота с cache-busting"""
        if self.main_screenshot:
            import time
            return f"{self.main_screenshot.url}?v={int(time.time())}"
        return ""
    
    @property
    def left_screenshot_url(self):
        """Возвращает URL левого скриншота с cache-busting"""
        if self.left_screenshot:
            import time
            return f"{self.left_screenshot.url}?v={int(time.time())}"
        return ""
    
    @property
    def right_screenshot_url(self):
        """Возвращает URL правого скриншота с cache-busting"""
        if self.right_screenshot:
            import time
            return f"{self.right_screenshot.url}?v={int(time.time())}"
        return ""