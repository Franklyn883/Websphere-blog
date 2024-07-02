# Generated by Django 4.2.6 on 2024-06-30 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blogpost", "0006_alter_post_options_category_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postcomment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_comments",
                to="blogpost.post",
            ),
        ),
    ]
