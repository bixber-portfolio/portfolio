# Generated by Django 3.2.16 on 2023-11-03 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
    ]
