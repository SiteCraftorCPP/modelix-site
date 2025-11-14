from django.core.management.base import BaseCommand
from main.models import HeroImage

class Command(BaseCommand):
    help = 'Создает дефолтное изображение первого блока'

    def handle(self, *args, **options):
        # Проверяем, есть ли уже запись
        if HeroImage.objects.exists():
            self.stdout.write(
                self.style.WARNING('Изображение первого блока уже существует')
            )
            return
        
        # Создаем дефолтную запись
        hero_image = HeroImage.objects.create(
            title='Главное изображение',
            image='services/hero_block.png',
            alt_text='3D принтер',
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано изображение первого блока: {hero_image.title}')
        )


class Command(BaseCommand):
    help = 'Создает дефолтное изображение первого блока'

    def handle(self, *args, **options):
        # Проверяем, есть ли уже запись
        if HeroImage.objects.exists():
            self.stdout.write(
                self.style.WARNING('Изображение первого блока уже существует')
            )
            return
        
        # Создаем дефолтную запись
        hero_image = HeroImage.objects.create(
            title='Главное изображение',
            image='services/hero_block.png',
            alt_text='3D принтер',
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано изображение первого блока: {hero_image.title}')
        )
