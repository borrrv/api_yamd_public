# Generated by Django 2.2.16 on 2022-11-21 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221121_1145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=None, null=True, verbose_name='Рейтинг'),
        ),
    ]
