# Generated by Django 4.2.10 on 2024-02-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_author_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='Viršelis'),
        ),
    ]
