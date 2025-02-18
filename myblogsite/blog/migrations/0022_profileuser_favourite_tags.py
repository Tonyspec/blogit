# Generated by Django 4.2 on 2025-01-18 19:56

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        ("blog", "0021_alter_post_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="profileuser",
            name="favourite_tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
