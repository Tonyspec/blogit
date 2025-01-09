from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_category_post_category'),  # Replace with the actual last migration
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(
                'Category',  # Assuming Category model is in the same app, if not, use 'app_name.Category'
                on_delete=models.CASCADE,
                related_name='posts',
                default=1  # Make sure category with id=1 exists in your database
            ),
        ),
    ]