# Generated by Django 4.2.6 on 2023-12-01 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0003_alter_postcomment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='comment',
            field=models.TextField(max_length=1000),
        ),
    ]
