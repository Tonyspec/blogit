# Generated by Django 4.2 on 2025-01-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0020_auto_20250118_1757"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
