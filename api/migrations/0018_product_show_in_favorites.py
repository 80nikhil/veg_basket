from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_order_block_flat_user_block_flat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_in_favorites',
            field=models.BooleanField(default=False),
        ),
    ]
