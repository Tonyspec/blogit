# Generated by Django 4.2 on 2025-01-15 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_post_summary_paragraph"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Paragraph",
        ),
    ]
