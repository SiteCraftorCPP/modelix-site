# Generated manually

from django.db import migrations


def update_marketplace_text_data(apps, schema_editor):
    ProjectsBlock = apps.get_model('main', 'ProjectsBlock')
    ProjectsBlock.objects.filter(
        marketplace_text='Мы выпускаем готовую продукцию. Отзывы, готовую продукцию и многое другое вы можете посмотреть на наших площадках'
    ).update(
        marketplace_text='Также, помимо индивидуальных проектов, мы выпускаем готовую продукцию; оценить её качество и прочитать отзывы можно на наших онлайн-витринах.'
    )


def reverse_update_marketplace_text_data(apps, schema_editor):
    ProjectsBlock = apps.get_model('main', 'ProjectsBlock')
    ProjectsBlock.objects.filter(
        marketplace_text='Также, помимо индивидуальных проектов, мы выпускаем готовую продукцию; оценить её качество и прочитать отзывы можно на наших онлайн-витринах.'
    ).update(
        marketplace_text='Мы выпускаем готовую продукцию. Отзывы, готовую продукцию и многое другое вы можете посмотреть на наших площадках'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_projectsblock_marketplace_text'),
    ]

    operations = [
        migrations.RunPython(update_marketplace_text_data, reverse_update_marketplace_text_data),
    ]




