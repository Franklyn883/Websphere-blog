# Generated by Django 4.2.5 on 2023-09-25 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
