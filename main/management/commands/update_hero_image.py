from django.core.management.base import BaseCommand
from main.models import HeroImage
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Обновляет изображение hero блока'

    def add_arguments(self, parser):
        parser.add_argument('image_path', type=str, help='Путь к новому изображению')

    def handle(self, *args, **options):
        image_path = options['image_path']
        
        # Проверяем, что файл существует
        if not os.path.exists(image_path):
            self.stdout.write(
                self.style.ERROR(f'Файл {image_path} не найден!')
            )
            return
        
        # Получаем или создаем HeroImage
        hero_image, created = HeroImage.objects.get_or_create(
            defaults={
                'title': 'Главное изображение',
                'image': 'hero/hero_block1.png',
                'alt_text': '3D принтер',
                'is_active': True
            }
        )
        
        # Обновляем изображение
        hero_image.image = image_path
        hero_image.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Изображение обновлено: {hero_image.image.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'URL: {hero_image.image.url}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'URL с cache-bust: {hero_image.image_url_with_cache_bust}')
        )
