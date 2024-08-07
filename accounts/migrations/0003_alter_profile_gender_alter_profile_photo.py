# Generated by Django 4.2.6 on 2024-06-30 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_profile_bio_alter_profile_location_follower"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "Female"), ("O", "Others")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
