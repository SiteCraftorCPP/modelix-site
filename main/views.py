from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import PrintOrder, CallRequest, Service, SocialLink, ContactInfo, FAQ, HeroImage, Stat, MarketplaceLink, WorksBlock, ProjectsBlock
import json

def index(request):
    """Главная страница"""
    # Получаем данные для отображения
    marketplace_links_db = MarketplaceLink.objects.filter(is_active=True).order_by('order')  # Активные ссылки из базы
    
    # Создаем список всех доступных платформ с дефолтными значениями
    PLATFORMS = [
        {'platform': 'vk_group', 'title': 'Группа ВКонтакте', 'icon': 'fab fa-vk', 'color': '#4680c2', 'url': '#'},
        {'platform': 'telegram', 'title': 'Telegram', 'icon': 'fab fa-telegram-plane', 'color': '#0088cc', 'url': '#'},
        {'platform': 'youtube', 'title': 'YouTube', 'icon': 'fab fa-youtube', 'color': '#ff0000', 'url': '#'},
        {'platform': 'ozon', 'title': 'Озон', 'icon': 'fas fa-shopping-bag', 'color': '#005BFF', 'url': '#'},
        {'platform': 'avito', 'title': 'Авито', 'icon': 'fas fa-store', 'color': '#FF6C37', 'url': '#'},
    ]
    
    # Создаем словарь ссылок из базы для быстрого поиска
    links_dict = {link.platform: link for link in marketplace_links_db}
    
    # Формируем финальный список: если есть в базе - используем данные из базы, иначе дефолтные
    marketplace_links = []
    for platform_data in PLATFORMS:
        if platform_data['platform'] in links_dict:
            link = links_dict[platform_data['platform']]
            marketplace_links.append({
                'url': link.url,
                'title': link.title,
                'icon': link.get_icon_class(),
                'color': link.get_platform_color(),
                'description': link.description if link.description else None,
            })
        else:
            marketplace_links.append({
                'url': platform_data['url'],
                'title': platform_data['title'],
                'icon': platform_data['icon'],
                'color': platform_data['color'],
                'description': None,
            })
    
    services = Service.objects.filter(is_active=True).order_by('order')  # Активные услуги
    if not services.exists():
        # Создаем дефолтные услуги если их нет (без описаний - пользователь добавит сам)
        Service.objects.create(
            service_type='3d_modeling',
            title='3D моделирование',
            description='',
            image=None,
            is_active=True,
            order=1
        )
        Service.objects.create(
            service_type='3d_printing',
            title='3D печать',
            description='',
            image=None,
            is_active=True,
            order=2
        )
        Service.objects.create(
            service_type='3d_scanning',
            title='3D сканирование',
            description='',
            image=None,
            is_active=True,
            order=3
        )
        Service.objects.create(
            service_type='reverse_engineering',
            title='Реверс-инжиниринг',
            description='',
            image=None,
            is_active=True,
            order=4
        )
        Service.objects.create(
            service_type='engineering',
            title='Инжиниринг',
            description='',
            image=None,
            is_active=True,
            order=5
        )
        Service.objects.create(
            service_type='post_processing',
            title='Постобработка',
            description='',
            image=None,
            is_active=True,
            order=6
        )
        services = Service.objects.filter(is_active=True).order_by('order')
    social_links = SocialLink.objects.filter(is_active=True).order_by('order')  # Активные социальные ссылки
    faq_items = FAQ.objects.filter(is_active=True).order_by('order')  # Активные FAQ
    
    # Получаем контактную информацию (создаем если не существует)
    contact_info, created = ContactInfo.objects.get_or_create(
        defaults={
            'phone': '+7 (929) 178-20-00',
            'email': 'modelix.stl@gmail.com',
            'work_hours': 'ПН-ПТ 10:00-20:00',
            'owner_name': 'ИП Худолей Илья Константинович',
            'inn': '780618190040'
        }
    )
    
    # Получаем hero изображение (берем первое активное или создаем новое)
    try:
        hero_image = HeroImage.objects.filter(is_active=True).first()
        if not hero_image:
            hero_image = HeroImage.objects.create(
                title='Главное изображение',
                image='hero/hero_block1_v5qOCbx_TEgQx6C.png',
                alt_text='3D принтер',
                is_active=True
            )
    except Exception:
        hero_image = None
    
    # Получаем статистику (создаем если не существует)
    stats = Stat.objects.filter(is_active=True).order_by('order')
    if not stats.exists():
        # Создаем дефолтные записи статистики
        Stat.objects.create(
            stat_type='experience',
            number='3+',
            label='Лет опыта.',
            icon_class='fa-calendar-alt',
            order=1
        )
        Stat.objects.create(
            stat_type='orders',
            number='100+',
            label='Успешно выполненных заказов.',
            icon_class='fa-check-circle',
            order=2
        )
        Stat.objects.create(
            stat_type='technologies',
            number='4+',
            label='Технологии печати.',
            icon_class='fa-cube',
            order=3
        )
        stats = Stat.objects.filter(is_active=True).order_by('order')
    
    # Получаем блок "Наши работы" (старый)
    works_block = WorksBlock.get_instance()
    
    # Получаем блок "НАШИ ПРОЕКТЫ" (новый)
    projects_block = ProjectsBlock.get_instance()
    
    # Получаем ссылки для мини-иконок и маркетплейсов в блоке проектов
    phone_links = {}
    phone_platforms = ['telegram', 'youtube', 'vk_group', 'avito', 'ozon']
    for platform in phone_platforms:
        try:
            link = MarketplaceLink.objects.get(platform=platform, is_active=True)
            phone_links[platform] = {
                'url': link.url,
                'title': link.title,
                'icon': link.get_icon_class(),
                'color': link.get_platform_color(),
            }
        except MarketplaceLink.DoesNotExist:
            # Дефолтные значения если нет в базе
            defaults = {
                'telegram': {'url': '#', 'title': 'Telegram', 'icon': 'fab fa-telegram-plane', 'color': '#0088cc'},
                'youtube': {'url': '#', 'title': 'YouTube', 'icon': 'fab fa-youtube', 'color': '#ff0000'},
                'vk_group': {'url': '#', 'title': 'ВКонтакте', 'icon': 'fab fa-vk', 'color': '#4680c2'},
                'avito': {'url': '#', 'title': 'Авито', 'icon': 'fas fa-store', 'color': '#FF6C37'},
                'ozon': {'url': '#', 'title': 'Озон', 'icon': 'fas fa-shopping-bag', 'color': '#005BFF'},
            }
            phone_links[platform] = defaults.get(platform, {'url': '#', 'title': platform, 'icon': 'fas fa-link', 'color': '#191970'})
    
    context = {
        'marketplace_links': marketplace_links,
        'services': services,
        'social_links': social_links,
        'contact_info': contact_info,
        'faq_items': faq_items,
        'hero_image': hero_image,
        'stats': stats,
        'works_block': works_block,
        'projects_block': projects_block,
        'phone_links': phone_links,
    }
    
    return render(request, 'main/index.html', context)

def submit_order(request):
    """Обработка заявки на печать"""
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()
            service_type = request.POST.get('service_type', 'other').strip()
            file = request.FILES.get('file')
            
            
            if not all([name, phone, email]):
                return JsonResponse({'success': False, 'error': 'Заполните все обязательные поля'})
            
            order = PrintOrder.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message,
                service_type=service_type,
                file=file
            )
            
            # Также сохраняем информацию о звонке в CallRequest
            if name and phone:
                CallRequest.objects.create(
                    name=name,
                    phone=phone
            )
            
            return JsonResponse({'success': True, 'message': 'Заявка успешно отправлена!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Произошла ошибка: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})



def submit_call_request(request):
    """Обработка заявки на звонок"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            if not all([name, phone]):
                return JsonResponse({'success': False, 'error': 'Заполните все поля'})
            
            call_request = CallRequest.objects.create(
                name=name,
                phone=phone
            )
            
            return JsonResponse({'success': True, 'message': 'Заявка на звонок принята!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Произошла ошибка при отправке заявки'})
    
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})