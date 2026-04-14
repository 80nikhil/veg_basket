from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_product_show_in_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='show_in_favorites',
        ),
        migrations.AddField(
            model_name='product',
            name='favorite_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Favorite Vegetable'), (1, 'Favorite Fruit')], null=True),
        ),
    ]
