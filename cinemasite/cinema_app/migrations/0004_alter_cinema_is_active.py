# Generated by Django 5.0.6 on 2024-06-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0003_alter_cinema_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='is_active',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Активный')], default=1),
        ),
    ]