# Generated by Django 5.0.6 on 2024-06-05 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0004_alter_cinema_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150)),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cinema',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Cinema', to='cinema_app.category'),
        ),
    ]
