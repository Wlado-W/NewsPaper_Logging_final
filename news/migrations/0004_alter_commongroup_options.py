# Generated by Django 3.2.12 on 2023-10-14 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_commongroup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commongroup',
            options={'verbose_name': 'common', 'verbose_name_plural': 'common'},
        ),
    ]
