# Generated by Django 2.2.16 on 2022-11-23 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Рейтинг выставляется по 10 бальной шкале.'), django.core.validators.MaxValueValidator(10, 'Рейтинг выставляется по 10 бальной шкале.')], verbose_name='Рейтинг'),
        ),
    ]
