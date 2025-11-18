# Generated manually

from django.db import migrations


def update_intro_text(apps, schema_editor):
    ProjectsBlock = apps.get_model('main', 'ProjectsBlock')
    ProjectsBlock.objects.filter(
        intro_text='Отслеживайте наши проекты в социальных сетях.'
    ).update(
        intro_text='С примерами проектов и тем, как мы их реализуем, можно ознакомиться в наших соцсетях.'
    )


def reverse_update_intro_text(apps, schema_editor):
    ProjectsBlock = apps.get_model('main', 'ProjectsBlock')
    ProjectsBlock.objects.filter(
        intro_text='С примерами проектов и тем, как мы их реализуем, можно ознакомиться в наших соцсетях.'
    ).update(
        intro_text='Отслеживайте наши проекты в социальных сетях.'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20251116_1646'),
    ]

    operations = [
        migrations.RunPython(update_intro_text, reverse_update_intro_text),
    ]

